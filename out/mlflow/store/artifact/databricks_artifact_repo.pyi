from _typeshed import Incomplete
from mlflow.azure.client import patch_adls_file_upload as patch_adls_file_upload, patch_adls_flush as patch_adls_flush, put_adls_file_creation as put_adls_file_creation, put_block as put_block, put_block_list as put_block_list
from mlflow.entities import FileInfo as FileInfo
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_artifacts_pb2 import ArtifactCredentialType as ArtifactCredentialType, DatabricksMlflowArtifactsService as DatabricksMlflowArtifactsService, GetCredentialsForRead as GetCredentialsForRead, GetCredentialsForWrite as GetCredentialsForWrite
from mlflow.protos.databricks_pb2 import INTERNAL_ERROR as INTERNAL_ERROR, INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.protos.service_pb2 import GetRun as GetRun, ListArtifacts as ListArtifacts, MlflowService as MlflowService
from mlflow.store.artifact.artifact_repo import ArtifactRepository as ArtifactRepository
from mlflow.utils import chunk_list as chunk_list, rest_utils as rest_utils
from mlflow.utils.databricks_utils import get_databricks_host_creds as get_databricks_host_creds
from mlflow.utils.file_utils import download_file_using_http_uri as download_file_using_http_uri, relative_path_to_artifact_path as relative_path_to_artifact_path, yield_file_in_chunks as yield_file_in_chunks
from mlflow.utils.proto_json_utils import message_to_json as message_to_json
from mlflow.utils.rest_utils import augmented_raise_for_status as augmented_raise_for_status, call_endpoint as call_endpoint, extract_api_info_for_service as extract_api_info_for_service
from mlflow.utils.uri import extract_and_normalize_path as extract_and_normalize_path, get_databricks_profile_uri_from_artifact_uri as get_databricks_profile_uri_from_artifact_uri, is_databricks_acled_artifacts_uri as is_databricks_acled_artifacts_uri, is_valid_dbfs_uri as is_valid_dbfs_uri, remove_databricks_profile_info_from_artifact_uri as remove_databricks_profile_info_from_artifact_uri

class DatabricksArtifactRepository(ArtifactRepository):
    databricks_profile_uri: Incomplete
    run_id: Incomplete
    run_relative_artifact_repo_root_path: Incomplete
    def __init__(self, artifact_uri) -> None: ...
    def log_artifact(self, local_file, artifact_path: Incomplete | None = None) -> None: ...
    def log_artifacts(self, local_dir, artifact_path: Incomplete | None = None) -> None: ...
    def list_artifacts(self, path: Incomplete | None = None): ...
    def delete_artifacts(self, artifact_path: Incomplete | None = None) -> None: ...
