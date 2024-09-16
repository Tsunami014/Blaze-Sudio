from _typeshed import Incomplete
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import BAD_REQUEST as BAD_REQUEST, INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE

class MetricThreshold:
    def __init__(self, threshold: Incomplete | None = None, min_absolute_change: Incomplete | None = None, min_relative_change: Incomplete | None = None, higher_is_better: Incomplete | None = None) -> None: ...
    @property
    def threshold(self): ...
    @property
    def min_absolute_change(self): ...
    @property
    def min_relative_change(self): ...
    @property
    def higher_is_better(self): ...

class MetricThresholdClassException(MlflowException):
    def __init__(self, _message, **kwargs) -> None: ...

class _MetricValidationResult:
    missing_candidate: bool
    missing_baseline: bool
    threshold_failed: bool
    min_absolute_change_failed: bool
    min_relative_change_failed: bool
    metric_name: Incomplete
    candidate_metric_value: Incomplete
    baseline_metric_value: Incomplete
    metric_threshold: Incomplete
    def __init__(self, metric_name, candidate_metric_value, metric_threshold, baseline_metric_value: Incomplete | None = None) -> None: ...
    def is_success(self): ...

class ModelValidationFailedException(MlflowException):
    def __init__(self, message, **kwargs) -> None: ...
