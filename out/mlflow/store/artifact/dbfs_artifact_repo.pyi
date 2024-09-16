from _typeshed import Incomplete
from mlflow.entities import FileInfo as FileInfo
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.store.artifact.artifact_repo import ArtifactRepository as ArtifactRepository
from mlflow.store.artifact.databricks_artifact_repo import DatabricksArtifactRepository as DatabricksArtifactRepository
from mlflow.store.artifact.local_artifact_repo import LocalArtifactRepository as LocalArtifactRepository
from mlflow.store.tracking.rest_store import RestStore as RestStore
from mlflow.tracking._tracking_service import utils as utils
from mlflow.utils.databricks_utils import get_databricks_host_creds as get_databricks_host_creds
from mlflow.utils.file_utils import relative_path_to_artifact_path as relative_path_to_artifact_path
from mlflow.utils.rest_utils import RESOURCE_DOES_NOT_EXIST as RESOURCE_DOES_NOT_EXIST, http_request as http_request, http_request_safe as http_request_safe
from mlflow.utils.string_utils import strip_prefix as strip_prefix
from mlflow.utils.uri import get_databricks_profile_uri_from_artifact_uri as get_databricks_profile_uri_from_artifact_uri, is_databricks_acled_artifacts_uri as is_databricks_acled_artifacts_uri, is_databricks_model_registry_artifacts_uri as is_databricks_model_registry_artifacts_uri, is_valid_dbfs_uri as is_valid_dbfs_uri, remove_databricks_profile_info_from_artifact_uri as remove_databricks_profile_info_from_artifact_uri

LIST_API_ENDPOINT: str
GET_STATUS_ENDPOINT: str
DOWNLOAD_CHUNK_SIZE: int
USE_FUSE_ENV_VAR: str

class DbfsRestArtifactRepository(ArtifactRepository):
    get_host_creds: Incomplete
    def __init__(self, artifact_uri) -> None: ...
    def log_artifact(self, local_file, artifact_path: Incomplete | None = None) -> None: ...
    def log_artifacts(self, local_dir, artifact_path: Incomplete | None = None) -> None: ...
    def list_artifacts(self, path: Incomplete | None = None): ...
    def delete_artifacts(self, artifact_path: Incomplete | None = None) -> None: ...

def dbfs_artifact_repo_factory(artifact_uri): ...
