from _typeshed import Incomplete
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.pipelines.cards import BaseCard as BaseCard
from mlflow.pipelines.step import BaseStep as BaseStep, StepClass as StepClass
from mlflow.pipelines.steps.train import TrainStep as TrainStep
from mlflow.pipelines.utils.execution import get_step_output_path as get_step_output_path
from mlflow.pipelines.utils.step import get_merged_eval_metrics as get_merged_eval_metrics
from mlflow.pipelines.utils.tracking import TrackingConfig as TrackingConfig, apply_pipeline_tracking_config as apply_pipeline_tracking_config, get_pipeline_tracking_config as get_pipeline_tracking_config, get_run_tags_env_vars as get_run_tags_env_vars
from mlflow.projects.utils import get_databricks_env_vars as get_databricks_env_vars
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.utils.databricks_utils import get_databricks_run_url as get_databricks_run_url
from typing import Any, NamedTuple

class MetricValidationResult(NamedTuple):
    metric: Incomplete
    greater_is_better: Incomplete
    value: Incomplete
    threshold: Incomplete
    validated: Incomplete

class EvaluateStep(BaseStep):
    tracking_config: Incomplete
    def __init__(self, step_config: dict[str, Any], pipeline_root: str) -> None: ...
    @classmethod
    def from_pipeline_config(cls, pipeline_config, pipeline_root): ...
    @property
    def name(self): ...
    @property
    def environment(self): ...
    def step_class(self): ...
