
"""Python Dataflow error class"""


class RondsError(Exception):
    """Base class for all Ronds errors"""


class PipelineError(RondsError):
    """An error in the pipeline object (e.g. a PValue not linked to it)."""


class PValueError(RondsError):
    """An error related to a PValue object (e.g. value is not computed)."""


class RunnerError(RondsError):
    """An error related to a Runner object (e.g. cannot find a runner to run)."""


class RuntimeValueProviderError(RuntimeError):
    """An error related to a ValueProvider object raised during runtime."""


class SideInputError(RondsError):
    """An error related to a side input to a parallel Do operation."""


class TransformError(RondsError):
    """An error related to a PTransform object."""


class KafkaError(RondsError):
    """An error related to a Kafka"""
