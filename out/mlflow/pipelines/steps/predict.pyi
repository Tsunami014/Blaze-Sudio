from _typeshed import Incomplete
from mlflow.exceptions import BAD_REQUEST as BAD_REQUEST, INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE, MlflowException as MlflowException
from mlflow.pipelines.artifacts import DataframeArtifact as DataframeArtifact, RegisteredModelVersionInfo as RegisteredModelVersionInfo
from mlflow.pipelines.cards import BaseCard as BaseCard
from mlflow.pipelines.step import BaseStep as BaseStep, StepClass as StepClass
from mlflow.pipelines.utils.execution import get_step_output_path as get_step_output_path
from mlflow.pipelines.utils.step import get_pandas_data_profiles as get_pandas_data_profiles
from mlflow.pipelines.utils.tracking import TrackingConfig as TrackingConfig, apply_pipeline_tracking_config as apply_pipeline_tracking_config, get_pipeline_tracking_config as get_pipeline_tracking_config
from mlflow.projects.utils import get_databricks_env_vars as get_databricks_env_vars
from mlflow.utils.file_utils import write_spark_dataframe_to_parquet_on_local_disk as write_spark_dataframe_to_parquet_on_local_disk
from typing import Any

class PredictStep(BaseStep):
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
