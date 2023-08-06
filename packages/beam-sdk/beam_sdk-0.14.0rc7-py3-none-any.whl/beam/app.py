import os
import json
import copy
from marshmallow import ValidationError
from typing import Any, List, Union, Optional
from importlib.metadata import version
from beam.utils.parse import compose_cpu, compose_memory, load_requirements_file
from beam.serializer import AppConfiguration
from beam.type import (
    PythonVersion,
    AutoscalingType,
    VolumeType,
    GpuType,
    BeamSerializeMode,
    TriggerType,
)


workspace_root = os.path.abspath(os.curdir)
sdk_version = version("beam-sdk")
BEAM_SERIALIZE_MODE = os.getenv("BEAM_SERIALIZE_MODE", None)


class Image:
    def __init__(
        self,
        python_version: PythonVersion = PythonVersion.Python38,
        python_packages: Union[List[str], str] = [],
        commands: List[str] = [],
    ):
        self.python_version = python_version
        self.python_packages = python_packages
        self.commands = commands

    @property
    def data(self):
        python_packages = copy.deepcopy(self.python_packages)
        if isinstance(python_packages, str):
            python_packages = load_requirements_file(python_packages)

        # We inject the current version of beam into here if does not exist
        if len([pkg for pkg in python_packages if "beam-sdk" in pkg]) == 0:
            python_packages.append(f"beam-sdk=={sdk_version}")

        return {
            "python_version": self.python_version,
            "python_packages": python_packages,
            "commands": self.commands,
        }

    @staticmethod
    def build_config(image: Union["Image", dict]):
        if isinstance(image, Image):
            return image.data
        else:
            return Image(
                **image,
            ).data


class Runtime:
    def __init__(
        self,
        cpu: Union[int, str] = 1,
        memory: str = "500Mi",
        gpu: Union[GpuType, str] = "",
        image: Union[Image, dict] = Image(),
    ):
        self.cpu = compose_cpu(cpu)
        self.memory = compose_memory(memory)
        self.gpu = gpu
        self.image = image

    @property
    def data(self):
        return {
            "cpu": self.cpu,
            "memory": self.memory,
            "gpu": self.gpu,
            "image": Image.build_config(self.image),
        }

    @staticmethod
    def build_config(runtime: Union["Runtime", dict]):
        if isinstance(runtime, Runtime):
            return runtime.data
        else:
            return Runtime(
                **runtime,
            ).data


class Output:
    def __init__(self, path: str) -> None:
        self.path = path

    @property
    def data(self):
        return {
            "path": self.path,
        }

    @staticmethod
    def build_config(output: Union["Output", dict]):
        if isinstance(output, Output):
            return output.data
        else:
            return Output(
                **output,
            ).data


class Autoscaling:
    def __init__(
        self,
        max_replicas: int = 1,
        desired_latency: float = 100,
        autoscaling_type: AutoscalingType = AutoscalingType.MaxRequestLatency,
    ):
        self.max_replicas = max_replicas
        self.desired_latency = desired_latency
        self.autoscaling_type = autoscaling_type

    @property
    def data(self):
        return {
            "max_replicas": self.max_replicas,
            "desired_latency": self.desired_latency,
            "autoscaling_type": self.autoscaling_type,
        }

    @staticmethod
    def build_config(autoscaling: Union["Autoscaling", dict]):
        if isinstance(autoscaling, Autoscaling):
            return autoscaling.data
        else:
            return Autoscaling(
                **autoscaling,
            ).data


class FunctionTrigger:
    def __init__(
        self,
        trigger_type: str,
        handler: str,
        runtime: Union[Runtime, dict] = None,
        outputs: List[Union[Output, dict]] = [],
        **kwargs,
    ):
        self.trigger_type = trigger_type
        self.kwargs = kwargs
        self.runtime = runtime
        self.handler = handler
        self.outputs = outputs
        self.autoscaling = kwargs.get("autoscaling", None)

    @property
    def data(self):
        return {
            **self.kwargs,
            "handler": self.handler,
            "runtime": Runtime.build_config(self.runtime) if self.runtime else None,
            "trigger_type": self.trigger_type,
            "outputs": [Output.build_config(output) for output in self.outputs],
            "autoscaling": Autoscaling.build_config(self.autoscaling)
            if self.autoscaling
            else None,
        }

    @staticmethod
    def build_config(trigger: Union["FunctionTrigger", dict]):
        if isinstance(trigger, FunctionTrigger):
            return trigger.data
        else:
            return FunctionTrigger(
                **trigger,
            ).data


class Run:
    def __init__(
        self,
        handler: str,
        runtime: Union[Runtime, dict],
        outputs: List[Union[Output, dict]] = [],
        **kwargs,
    ):
        self.kwargs = kwargs
        self.runtime = runtime
        self.handler = handler
        self.outputs = outputs

    @property
    def data(self):
        return {
            **self.kwargs,
            "handler": self.handler,
            "runtime": Runtime.build_config(self.runtime) if self.runtime else None,
            "outputs": [Output.build_config(output) for output in self.outputs],
        }

    @staticmethod
    def build_config(trigger: Union["Run", dict]):
        if isinstance(trigger, Run):
            return trigger.data
        else:
            return Run(
                **trigger,
            ).data


class Volume:
    def __init__(
        self, name: str, path: str, volume_type: VolumeType = VolumeType.Shared
    ):
        self.name = name
        self.app_path = path
        self.volume_type = volume_type

    @property
    def data(self):
        return {
            "name": self.name,
            "app_path": self.app_path,
            "mount_type": self.volume_type,
        }

    @staticmethod
    def build_config(volume: Union["Volume", dict]):
        if isinstance(volume, Volume):
            return volume.data
        else:
            return Volume(
                **volume,
            ).data


class App:
    def __init__(
        self,
        name: str,
        volumes: List[Union[Volume, dict]] = [],
        runtime: Union[Runtime, dict] = None,
    ):
        self.name = name
        self.volumes = []
        self.triggers = []
        self.runtime = runtime
        self.volumes = volumes

    def _function_metadata(self, func):
        f_dir = func.__code__.co_filename.replace(workspace_root, "").strip("/")
        f_name = func.__name__

        return f_dir, f_name

    def _parse_path(self, path: str, handler: str = ""):
        parsed_path = path
        if parsed_path is None:
            parsed_path = handler.split(":")[1]

        if not parsed_path.startswith("/"):
            parsed_path = "/" + parsed_path

        return parsed_path

    def build_config(
        self,
        triggers: List[Union[FunctionTrigger, dict]] = [],
        run: Optional[dict] = None,
    ):
        if (len(triggers) == 0) == bool(run is None):
            raise ValidationError("Provide either triggers or a run, but not both")

        serialized_triggers = []
        for trigger in triggers:
            serialized_trigger = FunctionTrigger.build_config(trigger)
            if serialized_trigger["runtime"] is None and self.runtime is None:
                raise ValidationError(
                    "Runtime must be specified for all triggers if not specified at the app level"
                )
            serialized_triggers.append(serialized_trigger)

        serialized_run = None
        if run is not None:
            serialized_run = Run.build_config(run)
            if serialized_run["runtime"] is None and self.runtime is None:
                raise ValidationError(
                    "Runtime must be specified for the run if not specified at the app level"
                )

        config = {
            "app_spec_version": "v3",
            "sdk_version": sdk_version,
            "name": self.name,
            "mounts": [Volume.build_config(volume) for volume in self.volumes],
            "runtime": Runtime.build_config(self.runtime) if self.runtime else None,
            "triggers": serialized_triggers,
            "run": serialized_run,
        }

        serializer = AppConfiguration()
        # convert orderdict to a dict that's still ordered
        return json.loads(json.dumps(serializer.load(config)))

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if BEAM_SERIALIZE_MODE in [BeamSerializeMode.Start, BeamSerializeMode.Deploy]:
            return self.build_config(triggers=self.triggers)

        elif BEAM_SERIALIZE_MODE == BeamSerializeMode.Run:
            raise ValidationError("Cannot run an app. Please run a function instead.")

    def task_queue(
        self,
        path: Optional[str] = None,
        runtime: Union[dict, Runtime] = None,
        outputs: List[Union[Output, dict]] = [],
        autoscaling: Union[dict, Autoscaling] = None,
        loader: Optional[str] = None,
        callback_url: Optional[str] = None,
        max_pending_tasks: Optional[int] = 100,
        keep_warm_seconds: Optional[int] = 0,
        method: str = "POST",
    ):
        def decorator(func):
            f_dir, f_name = self._function_metadata(func)
            handler = f"{f_dir}:{f_name}"
            parsed_path = self._parse_path(path, handler)
            config_data = {
                "trigger_type": TriggerType.Webhook,
                "handler": handler,
                "method": method,
                "runtime": runtime,
                "outputs": outputs,
                "autoscaling": autoscaling,
                "path": parsed_path,
                "loader": loader,
                "callback_url": callback_url,
                "max_pending_tasks": max_pending_tasks,
                "keep_warm_seconds": keep_warm_seconds,
            }

            task_queue = FunctionTrigger(**config_data)
            self.triggers.append(task_queue)

            def wrapper(*args, **kwargs):
                if BEAM_SERIALIZE_MODE in [
                    BeamSerializeMode.Start,
                    BeamSerializeMode.Deploy,
                ]:
                    return self.build_config(triggers=[task_queue])

                elif BEAM_SERIALIZE_MODE == BeamSerializeMode.Run:
                    return self.build_config(run=Run(**config_data))

                return func(*args, **kwargs)

            return wrapper

        return decorator

    def rest_api(
        self,
        path: Optional[str] = None,
        runtime: Union[dict, Runtime] = None,
        outputs: List[Union[Output, dict]] = [],
        autoscaling: Union[dict, Autoscaling] = None,
        loader: Optional[str] = None,
        callback_url: Optional[str] = None,
        max_pending_tasks: Optional[int] = 100,
        keep_warm_seconds: Optional[int] = 0,
        method: str = "POST",
    ):
        def decorator(func):
            f_dir, f_name = self._function_metadata(func)
            handler = f"{f_dir}:{f_name}"
            parsed_path = self._parse_path(path, handler)
            config_data = {
                "trigger_type": TriggerType.RestAPI,
                "handler": handler,
                "method": method,
                "runtime": runtime,
                "outputs": outputs,
                "autoscaling": autoscaling,
                "path": parsed_path,
                "loader": loader,
                "callback_url": callback_url,
                "max_pending_tasks": max_pending_tasks,
                "keep_warm_seconds": keep_warm_seconds,
            }

            rest_api = FunctionTrigger(**config_data)
            self.triggers.append(rest_api)

            def wrapper(*args, **kwargs):
                if BEAM_SERIALIZE_MODE in [
                    BeamSerializeMode.Start,
                    BeamSerializeMode.Deploy,
                ]:
                    return self.build_config(triggers=[rest_api])

                elif BEAM_SERIALIZE_MODE == BeamSerializeMode.Run:
                    return self.build_config(run=Run(**config_data))

                return func(*args, **kwargs)

            return wrapper

        return decorator

    def schedule(
        self,
        when: str,
        runtime: Union[dict, Runtime] = None,
        outputs: List[Union[Output, dict]] = [],
        callback_url: Optional[str] = None,
    ):
        def decorator(func):
            f_dir, f_name = self._function_metadata(func)
            config_data = {
                "when": when,
                "trigger_type": TriggerType.Schedule,
                "handler": f"{f_dir}:{f_name}",
                "runtime": runtime,
                "outputs": outputs,
                "callback_url": callback_url,
            }

            schedule = FunctionTrigger(
                **config_data,
            )
            self.triggers.append(schedule)

            def wrapper(*args, **kwargs):
                if BEAM_SERIALIZE_MODE in [
                    BeamSerializeMode.Start,
                    BeamSerializeMode.Deploy,
                ]:
                    return self.build_config(triggers=[schedule])

                elif BEAM_SERIALIZE_MODE == BeamSerializeMode.Run:
                    return self.build_config(run=Run(**config_data))

                return func(*args, **kwargs)

            return wrapper

        return decorator

    def run(
        self,
        runtime: Union[dict, Runtime] = None,
        outputs: List[Union[Output, dict]] = [],
        callback_url: Optional[str] = None,
    ):
        def decorator(func):
            f_dir, f_name = self._function_metadata(func)
            config_data = {
                "handler": f"{f_dir}:{f_name}",
                "runtime": runtime,
                "outputs": outputs,
                "callback_url": callback_url,
            }

            def wrapper(*args, **kwargs):
                if BEAM_SERIALIZE_MODE == BeamSerializeMode.Deploy:
                    raise ValidationError(
                        "Cannot deploy a run function. Use [beam run] instead."
                    )
                elif BEAM_SERIALIZE_MODE in [
                    BeamSerializeMode.Start,
                    BeamSerializeMode.Run,
                ]:
                    return self.build_config(run=Run(**config_data))

                return func(*args, **kwargs)

            return wrapper

        return decorator
