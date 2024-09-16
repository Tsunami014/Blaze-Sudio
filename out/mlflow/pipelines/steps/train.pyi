from _typeshed import Incomplete
from mlflow.entities import SourceType as SourceType, ViewType as ViewType
from mlflow.exceptions import BAD_REQUEST as BAD_REQUEST, INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE, MlflowException as MlflowException
from mlflow.pipelines.artifacts import HyperParametersArtifact as HyperParametersArtifact, ModelArtifact as ModelArtifact, RunArtifact as RunArtifact
from mlflow.pipelines.cards import BaseCard as BaseCard
from mlflow.pipelines.step import BaseStep as BaseStep, StepClass as StepClass
from mlflow.pipelines.utils.execution import get_step_output_path as get_step_output_path
from mlflow.pipelines.utils.step import get_merged_eval_metrics as get_merged_eval_metrics, get_pandas_data_profiles as get_pandas_data_profiles
from mlflow.pipelines.utils.tracking import TrackingConfig as TrackingConfig, apply_pipeline_tracking_config as apply_pipeline_tracking_config, get_pipeline_tracking_config as get_pipeline_tracking_config, get_run_tags_env_vars as get_run_tags_env_vars, log_code_snapshot as log_code_snapshot
from mlflow.projects.utils import get_databricks_env_vars as get_databricks_env_vars
from mlflow.tracking import MlflowClient as MlflowClient
from mlflow.utils.databricks_utils import get_databricks_run_url as get_databricks_run_url
from mlflow.utils.mlflow_tags import MLFLOW_PIPELINE_PROFILE_NAME as MLFLOW_PIPELINE_PROFILE_NAME, MLFLOW_PIPELINE_STEP_NAME as MLFLOW_PIPELINE_STEP_NAME, MLFLOW_PIPELINE_TEMPLATE_NAME as MLFLOW_PIPELINE_TEMPLATE_NAME, MLFLOW_SOURCE_TYPE as MLFLOW_SOURCE_TYPE

class TrainStep(BaseStep):
    MODEL_ARTIFACT_RELATIVE_PATH: str
    tracking_config: Incomplete
    pipeline_config: Incomplete
    def __init__(self, step_config, pipeline_root, pipeline_config: Incomplete | None = None) -> None: ...
    @classmethod
    def construct_search_space_from_yaml(cls, params): ...
    @classmethod
    def is_tuning_param_equal(cls, tuning_param, logged_param): ...
    @classmethod
    def from_pipeline_config(cls, pipeline_config, pipeline_root): ...
    @property
    def name(self): ...
    @property
    def environment(self): ...
    def get_artifacts(self): ...
    def step_class(self): ...
