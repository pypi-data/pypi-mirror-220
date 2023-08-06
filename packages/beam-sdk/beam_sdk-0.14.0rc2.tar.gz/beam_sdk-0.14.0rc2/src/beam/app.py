import os
import json
from marshmallow import ValidationError
from typing import Any, List, Union, Optional, Literal
from beam.utils.print import print_config
from beam.utils.parse import compose_cpu, compose_memory
from beam.serializer import AppConfiguration
from beam.type import (
    PythonVersion,
    AutoscalingType,
    OutputType,
    VolumeType,
    GpuType,
) 
    

workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Image:
    """
    Image is a class that represents the image configuration for a Beam application.
    kwargs:
        python_version: 
            Specifies the python version that will be downloaded by the image.
            Currently only supports Python [3.7, 3.8, 3.9, and 3.10]
        python_packages: 


        commands: List[str] = []
    
    """
    def __init__(
        self,
        python_version: PythonVersion = PythonVersion.Python38,
        python_packages: Union[List[str], str] = [],
        commands: List[str] = [],
    ):
        self.python_version = python_version
        self.python_packages = python_packages
        self.commands = commands

    def serialize(self):
        return {
            "python_version": self.python_version,
            "python_packages": self.python_packages,
            "commands": self.commands,
        }

    @staticmethod
    def build_config(image: Union["Image", dict]):
        if isinstance(image, Image):
            return image.serialize()
        else:
            return Image(
                **image,
            ).serialize()


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

    def serialize(self):
        return {
            "cpu": self.cpu,
            "memory": self.memory,
            "gpu": self.gpu,
            "image": Image.build_config(self.image),
        }

    @staticmethod
    def build_config(runtime: Union["Runtime", dict]):
        if isinstance(runtime, Runtime):
            return runtime.serialize()
        else:
            return Runtime(
                **runtime,
            ).serialize()


class Output:
    def __init__(
        self, name: str, path: str, output_type: OutputType
    ) -> None:
        self.name = name
        self.path = path
        self.output_type = output_type

    def serialize(self):
        return {
            "name": self.name,
            "path": self.path,
            "output_type": self.output_type,
        }

    @staticmethod
    def build_config(output: Union["Output", dict]):
        if isinstance(output, Output):
            return output.serialize()
        else:
            return Output(
                **output,
            ).serialize()


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

    def serialize(self):
        return {
            "max_replicas": self.max_replicas,
            "desired_latency": self.desired_latency,
            "autoscaling_type": self.autoscaling_type,
        }

    @staticmethod
    def build_config(autoscaling: Union["Autoscaling", dict]):
        if isinstance(autoscaling, Autoscaling):
            return autoscaling.serialize()
        else:
            return Autoscaling(
                **autoscaling,
            ).serialize()


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
        self.data = kwargs
        self.runtime = runtime
        self.handler = handler
        self.outputs = outputs

    def serialize(self):
        return {
            **self.data,
            "handler": self.handler,
            "runtime": Runtime.build_config(self.runtime) if self.runtime else None,
            "trigger_type": self.trigger_type,
            "outputs": [Output.build_config(output) for output in self.outputs],
            "autoscaling": Autoscaling.build_config(self.data.get("autoscaling"))
            if self.data.get("autoscaling")
            else None,
        }

    @staticmethod
    def build_config(trigger: Union["FunctionTrigger", dict]):
        if isinstance(trigger, FunctionTrigger):
            return trigger.serialize()
        else:
            return FunctionTrigger(
                **trigger,
            ).serialize()


class Run:
    def __init__(
        self,
        handler: str,
        runtime: Union[Runtime, dict],
        outputs: List[Union[Output, dict]] = [],
        **kwargs,
    ):
        self.data = kwargs
        self.runtime = runtime
        self.handler = handler
        self.outputs = outputs

    def serialize(self):
        return {
            **self.data,
            "handler": self.handler,
            "runtime": Runtime.build_config(self.runtime) if self.runtime else None,
            "outputs": [Output.build_config(output) for output in self.outputs],
        }

    @staticmethod
    def build_config(trigger: Union["Run", dict]):
        if isinstance(trigger, Run):
            return trigger.serialize()
        else:
            return Run(
                **trigger,
            ).serialize()


class Volume:
    def __init__(
        self, name: str, path: str, volume_type: VolumeType
    ):
        self.name = name
        self.app_path = path
        self.volume_type = volume_type

    def serialize(self):
        return {
            "name": self.name,
            "app_path": self.app_path,
            "mount_type": self.volume_type,
        }

    @staticmethod
    def build_config(volume: Union["Volume", dict]):
        if isinstance(volume, Volume):
            return volume.serialize()
        else:
            return Volume(
                **volume,
            ).serialize()


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
        self.run_object = None

    def _function_metadata(self, func):
        f_dir = func.__code__.co_filename.replace(workspace_root, "").strip("/")
        f_name = func.__name__

        return f_dir, f_name

    def build_config(
        self, triggers: List[Union[FunctionTrigger, dict]] = [], run: Optional[dict] = None
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
        if os.getenv("BEAM_SERIALIZE") == "1":
            output_text = json.dumps(
                self.build_config(triggers=self.triggers, run=self.run), indent=2
            )
            print_config(output_text)
            return output_text

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

            parsed_path = path
            if parsed_path is None:
                parsed_path = handler.split(":")[1]

            if not parsed_path.startswith("/"):
                parsed_path = "/" + parsed_path

            task_queue = FunctionTrigger(
                trigger_type="webhook",
                handler=handler,
                method=method,
                runtime=runtime,
                outputs=outputs,
                autoscaling=autoscaling,
                path=parsed_path,
                loader=loader,
                callback_url=callback_url,
                max_pending_tasks=max_pending_tasks,
                keep_warm_seconds=keep_warm_seconds,
            )
            self.triggers.append(task_queue)

            def wrapper(*args, **kwargs):
                if os.getenv("BEAM_SERIALIZE") == "1":
                    data = self.build_config(triggers=[task_queue])
                    output_text = json.dumps(data, indent=2)
                    print_config(output_text)
                    return data

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

            parsed_path = path
            if parsed_path is None:
                parsed_path = handler.split(":")[1]

            if not parsed_path.startswith("/"):
                parsed_path = "/" + parsed_path

            rest_api = FunctionTrigger(
                trigger_type="rest_api",
                handler=handler,
                method=method,
                runtime=runtime,
                outputs=outputs,
                autoscaling=autoscaling,
                path=parsed_path,
                loader=loader,
                callback_url=callback_url,
                max_pending_tasks=max_pending_tasks,
                keep_warm_seconds=keep_warm_seconds,
            )
            self.triggers.append(rest_api)

            def wrapper(*args, **kwargs):
                if os.getenv("BEAM_SERIALIZE") == "1":
                    data = self.build_config(triggers=[rest_api])
                    output_text = json.dumps(data, indent=2)
                    print_config(output_text)
                    return data

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
            schedule = FunctionTrigger(
                when=when,
                trigger_type="cron_job",
                handler=f"{f_dir}:{f_name}",
                runtime=runtime,
                outputs=outputs,
                callback_url=callback_url,
            )
            self.triggers.append(schedule)

            def wrapper(*args, **kwargs):
                if os.getenv("BEAM_SERIALIZE") == "1":
                    data = self.build_config(triggers=[schedule])
                    output_text = json.dumps(data, indent=2)
                    print_config(output_text)
                    return data

                return func(*args, **kwargs)

            return wrapper

        return decorator

    def run(
        self,
        name: Optional[str] = None,
        runtime: Union[dict, Runtime] = None,
        outputs: List[Union[Output, dict]] = [],
        callback_url: Optional[str] = None,
    ):
        def decorator(func):
            f_dir, f_name = self._function_metadata(func)
            run = Run(
                name=name,
                handler=f"{f_dir}:{f_name}",
                runtime=runtime,
                outputs=outputs,
                callback_url=callback_url,
            )
            self.run_object = run

            def wrapper(*args, **kwargs):
                if os.getenv("BEAM_SERIALIZE") == "1":
                    data = self.build_config(run=run)
                    output_text = json.dumps(data, indent=2)
                    print_config(output_text)
                    return data

                return func(*args, **kwargs)

            return wrapper

        return decorator
