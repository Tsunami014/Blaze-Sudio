from _typeshed import Incomplete
from mlflow.exceptions import MlflowException as MlflowException, RestException as RestException
from mlflow.pipelines.utils import get_pipeline_name as get_pipeline_name
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.tracking.client import MlflowClient as MlflowClient
from mlflow.tracking.context.registry import resolve_tags as resolve_tags
from mlflow.tracking.context.system_environment_context import MLFLOW_RUN_CONTEXT_ENV_VAR as MLFLOW_RUN_CONTEXT_ENV_VAR
from mlflow.tracking.default_experiment import DEFAULT_EXPERIMENT_ID as DEFAULT_EXPERIMENT_ID
from mlflow.utils.databricks_utils import is_in_databricks_runtime as is_in_databricks_runtime
from mlflow.utils.file_utils import path_to_local_file_uri as path_to_local_file_uri, path_to_local_sqlite_uri as path_to_local_sqlite_uri
from mlflow.utils.git_utils import get_git_branch as get_git_branch, get_git_commit as get_git_commit, get_git_repo_url as get_git_repo_url
from mlflow.utils.mlflow_tags import LEGACY_MLFLOW_GIT_REPO_URL as LEGACY_MLFLOW_GIT_REPO_URL, MLFLOW_GIT_BRANCH as MLFLOW_GIT_BRANCH, MLFLOW_GIT_COMMIT as MLFLOW_GIT_COMMIT, MLFLOW_GIT_REPO_URL as MLFLOW_GIT_REPO_URL, MLFLOW_SOURCE_NAME as MLFLOW_SOURCE_NAME
from typing import Any, TypeVar

TrackingConfigType = TypeVar('TrackingConfig')

class TrackingConfig:
    tracking_uri: Incomplete
    experiment_name: Incomplete
    experiment_id: Incomplete
    artifact_location: Incomplete
    def __init__(self, tracking_uri: str, experiment_name: str = None, experiment_id: str = None, artifact_location: str = None) -> None: ...
    def to_dict(self) -> dict[str, str]: ...
    @classmethod
    def from_dict(cls, config_dict: dict[str, str]) -> TrackingConfigType: ...

def get_pipeline_tracking_config(pipeline_root_path: str, pipeline_config: dict[str, Any]) -> TrackingConfig: ...
def apply_pipeline_tracking_config(tracking_config: TrackingConfig): ...
def get_run_tags_env_vars(pipeline_root_path: str) -> dict[str, str]: ...
def log_code_snapshot(pipeline_root: str, run_id: str, artifact_path: str = 'pipeline_snapshot', pipeline_config: dict[str, Any] = None) -> None: ...
