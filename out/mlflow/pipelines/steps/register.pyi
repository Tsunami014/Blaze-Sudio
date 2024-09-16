from _typeshed import Incomplete
from mlflow.entities import SourceType as SourceType
from mlflow.exceptions import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE, MlflowException as MlflowException
from mlflow.pipelines.artifacts import ModelVersionArtifact as ModelVersionArtifact, RegisteredModelVersionInfo as RegisteredModelVersionInfo
from mlflow.pipelines.cards import BaseCard as BaseCard
from mlflow.pipelines.step import BaseStep as BaseStep, StepClass as StepClass
from mlflow.pipelines.steps.train import TrainStep as TrainStep
from mlflow.pipelines.utils.execution import get_step_output_path as get_step_output_path
from mlflow.pipelines.utils.tracking import TrackingConfig as TrackingConfig, apply_pipeline_tracking_config as apply_pipeline_tracking_config, get_pipeline_tracking_config as get_pipeline_tracking_config
from mlflow.projects.utils import get_databricks_env_vars as get_databricks_env_vars
from mlflow.tracking._model_registry import DEFAULT_AWAIT_MAX_SLEEP_SECONDS as DEFAULT_AWAIT_MAX_SLEEP_SECONDS
from mlflow.utils.databricks_utils import get_databricks_model_version_url as get_databricks_model_version_url, get_databricks_run_url as get_databricks_run_url
from mlflow.utils.mlflow_tags import MLFLOW_PIPELINE_TEMPLATE_NAME as MLFLOW_PIPELINE_TEMPLATE_NAME, MLFLOW_SOURCE_TYPE as MLFLOW_SOURCE_TYPE
from typing import Any

class RegisterStep(BaseStep):
    tracking_config: Incomplete
    def __init__(self, step_config: dict[str, Any], pipeline_root: str) -> None: ...
    @classmethod
    def from_pipeline_config(cls, pipeline_config, pipeline_root): ...
    @property
    def name(self): ...
    @property
    def environment(self): ...
    def get_artifacts(self): ...
    def step_class(self): ...
