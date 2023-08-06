from typing import Callable
from marshmallow import validate
from beam.type import (
    PythonVersion,
    GpuType,
    TriggerType,
    OutputType,
    VolumeType,
    AutoscalingType,
)
from beam.utils.parse import compose_cpu, compose_memory
from beam import validators
from marshmallow import Schema, fields, ValidationError

class SerializerMethod(fields.Field):
    def __init__(self, method: Callable, **kwargs):
        self.method = method
        super().__init__(**kwargs)

    def serialize(self, value, attr, obj, **kwargs):
        try:
            return self.method(value)
        except Exception as e:
            raise ValidationError(str(e))

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return self.method(value)
        except Exception as e:
            raise ValidationError(str(e))

class ListOfStringOrString(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, list):
            return value
        elif isinstance(value, str):
            return value
        else:
            raise ValidationError("Invalid type. Expected list or string")


class AutoscalingConfiguration(Schema):
    max_replicas = fields.Integer(required=True)
    desired_latency = fields.Float(required=True)
    autoscaling_type = fields.String(
        validate=validate.OneOf(
            choices=[autoscaling[1] for autoscaling in AutoscalingType.Types]
        ),
        required=True,
    )

    class Meta:
        ordered = True


class VolumeConfiguration(Schema):
    name = fields.String(required=True)
    app_path = fields.String(required=True)
    mount_type = fields.String(
        validate=validate.OneOf(choices=[mount[1] for mount in VolumeType.Types]),
        required=True,
    )

    class Meta:
        ordered = True


class OutputConfiguration(Schema):
    name = fields.String(required=True)
    path = fields.String(required=True)
    output_type = fields.String(
        validate=validate.OneOf(choices=[output[1] for output in OutputType.Types]),
        required=True,
    )

    class Meta:
        ordered = True


class ImageConfiguration(Schema):
    python_version = fields.String(
        validate=validate.OneOf(
            choices=[version[1] for version in PythonVersion.Types]
        ),
        dump_default=PythonVersion.Python38,
    )
    python_packages = ListOfStringOrString()
    commands = fields.List(fields.String(), dump_default=[])

    class Meta:
        ordered = True


class RuntimeConfiguration(Schema):
    cpu = SerializerMethod(compose_cpu, required=True)
    memory = SerializerMethod(compose_memory, required=True)
    gpu = fields.String(
        validate=validate.OneOf(choices=[gpu[1] for gpu in GpuType.Types])
    )
    image = fields.Nested(ImageConfiguration, required=True)

    class Meta:
        ordered = True


class RunConfiguration(Schema):
    name = fields.String(allow_none=True)
    handler = fields.String(validate=validators.IsFileMethod(), required=True)
    callback_url = fields.Url(allow_none=True)
    outputs = fields.Nested(OutputConfiguration, dump_default=[], many=True)
    runtime = fields.Nested(RuntimeConfiguration, dump_default=None, allow_none=True)

    class Meta:
        ordered = True


class TriggerConfiguration(Schema):
    handler = fields.String(validate=validators.IsFileMethod(), required=True)
    loader = fields.String(
        validate=validators.IsFileMethod(),
        allow_none=True,
    )
    callback_url = fields.Url(
        allow_none=True,
    )
    max_pending_tasks = fields.Integer()
    keep_warm_seconds = fields.Integer()
    trigger_type = fields.String(
        validate=validate.OneOf(choices=[trigger[1] for trigger in TriggerType.Types]),
        required=True,
    )
    path = fields.String()
    method = fields.String(validate=validate.OneOf(choices=["GET", "POST"]))
    runtime = fields.Nested(RuntimeConfiguration, dump_default=None, allow_none=True)
    outputs = fields.Nested(OutputConfiguration, dump_default=[], many=True)
    autoscaling = fields.Nested(
        AutoscalingConfiguration, dump_default=None, allow_none=True
    )
    when = fields.String(
        validate=validators.IsValidCronOrEvery(), dump_default=None, allow_none=True
    )

    class Meta:
        ordered = True


class AppConfiguration(Schema):
    name = fields.String(required=True)
    runtime = fields.Nested(RuntimeConfiguration, dump_default=None, allow_none=True)
    volumes = fields.List(fields.Nested(VolumeConfiguration), dump_default=[])
    triggers = fields.Nested(TriggerConfiguration, dump_default=[], many=True)
    run = fields.Nested(RunConfiguration, dump_default=None, allow_none=True)

    class Meta:
        ordered = True
