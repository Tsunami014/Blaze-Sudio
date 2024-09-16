from mlflow.environment_variables import MLFLOW_TRACKING_AWS_SIGV4 as MLFLOW_TRACKING_AWS_SIGV4
from mlflow.store.db.db_types import DATABASE_ENGINES as DATABASE_ENGINES
from mlflow.store.model_registry.rest_store import RestStore as RestStore
from mlflow.tracking._model_registry.registry import ModelRegistryStoreRegistry as ModelRegistryStoreRegistry
from mlflow.tracking._tracking_service.utils import get_tracking_uri as get_tracking_uri
from mlflow.utils import rest_utils as rest_utils
from mlflow.utils.databricks_utils import get_databricks_host_creds as get_databricks_host_creds

def set_registry_uri(uri: str) -> None: ...
def get_registry_uri() -> str: ...
def get_default_host_creds(store_uri): ...
