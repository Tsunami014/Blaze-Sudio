from _typeshed import Incomplete
from mlflow.exceptions import BAD_REQUEST as BAD_REQUEST, MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE

class PipelineMetric:
    name: Incomplete
    greater_is_better: Incomplete
    custom_function: Incomplete
    def __init__(self, name: str, greater_is_better: bool, custom_function: str | None = None) -> None: ...
    @classmethod
    def from_custom_metric_dict(cls, custom_metric_dict): ...

BUILTIN_CLASSIFICATION_PIPELINE_METRICS: Incomplete
BUILTIN_REGRESSION_PIPELINE_METRICS: Incomplete
