from mlflow.environment_variables import MLFLOW_TRACKING_AWS_SIGV4 as MLFLOW_TRACKING_AWS_SIGV4
from mlflow.store.db.db_types import DATABASE_ENGINES as DATABASE_ENGINES
from mlflow.store.tracking import DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH as DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH
from mlflow.store.tracking.file_store import FileStore as FileStore
from mlflow.store.tracking.rest_store import DatabricksRestStore as DatabricksRestStore, RestStore as RestStore
from mlflow.tracking._tracking_service.registry import TrackingStoreRegistry as TrackingStoreRegistry
from mlflow.utils import env as env, rest_utils as rest_utils
from mlflow.utils.databricks_utils import get_databricks_host_creds as get_databricks_host_creds
from mlflow.utils.file_utils import path_to_local_file_uri as path_to_local_file_uri
from pathlib import Path

def is_tracking_uri_set(): ...
def set_tracking_uri(uri: str | Path) -> None: ...
def get_tracking_uri() -> str: ...
