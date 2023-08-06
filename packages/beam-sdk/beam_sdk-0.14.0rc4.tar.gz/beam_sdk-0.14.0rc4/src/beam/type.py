class TriggerType:
    Webhook = "webhook"
    RestAPI = "rest_api"
    Schedule = "cron_job"
    Types = ((Webhook, "webhook"), (RestAPI, "rest_api"), (Schedule, "cron_job"))


class PythonVersion:
    Python37 = "python3.7"
    Python38 = "python3.8"
    Python39 = "python3.9"
    Python310 = "python3.10"
    Types = (
        (Python37, "python3.7"),
        (Python38, "python3.8"),
        (Python39, "python3.9"),
        (Python310, "python3.10"),
    )


class GpuType:
    NoGPU = ""
    Any = "any"
    T4 = "T4"
    A10G = "A10G"
    Types = (
        (NoGPU, ""),
        (Any, "any"),
        (T4, "T4"),
        (A10G, "A10G"),
    )


class VolumeType:
    Persistent = "persistent"
    Shared = "shared"
    Types = (
        (Persistent, "persistent"),
        (Shared, "shared"),
    )


class AutoscalingType:
    MaxRequestLatency = "max_request_latency"
    Types = ((MaxRequestLatency, "max_request_latency"),)


class BeamSerializeMode:
    Deploy = "deploy"
    Start = "start"
    Run = "run"
    Stop = "stop"
    Serve = "serve"
