from _typeshed import Incomplete
from mlflow.entities import FileInfo as FileInfo
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.store.artifact.artifact_repo import ArtifactRepository as ArtifactRepository
from mlflow.store.artifact.utils.models import get_model_name_and_version as get_model_name_and_version, is_using_databricks_registry as is_using_databricks_registry
from mlflow.utils.databricks_utils import get_databricks_host_creds as get_databricks_host_creds
from mlflow.utils.file_utils import download_file_using_http_uri as download_file_using_http_uri
from mlflow.utils.rest_utils import http_request as http_request
from mlflow.utils.uri import get_databricks_profile_uri_from_artifact_uri as get_databricks_profile_uri_from_artifact_uri

REGISTRY_LIST_ARTIFACTS_ENDPOINT: str
REGISTRY_ARTIFACT_PRESIGNED_URI_ENDPOINT: str

class DatabricksModelsArtifactRepository(ArtifactRepository):
    databricks_profile_uri: Incomplete
    def __init__(self, artifact_uri) -> None: ...
    def list_artifacts(self, path: Incomplete | None = None): ...
    def log_artifact(self, local_file, artifact_path: Incomplete | None = None) -> None: ...
    def log_artifacts(self, local_dir, artifact_path: Incomplete | None = None) -> None: ...
    def delete_artifacts(self, artifact_path: Incomplete | None = None) -> None: ...
