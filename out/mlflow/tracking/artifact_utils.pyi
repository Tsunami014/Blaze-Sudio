from _typeshed import Incomplete
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.store.artifact.artifact_repository_registry import get_artifact_repository as get_artifact_repository
from mlflow.store.artifact.dbfs_artifact_repo import DbfsRestArtifactRepository as DbfsRestArtifactRepository
from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository as ModelsArtifactRepository
from mlflow.utils.file_utils import path_to_local_file_uri as path_to_local_file_uri
from mlflow.utils.uri import add_databricks_profile_info_to_artifact_uri as add_databricks_profile_info_to_artifact_uri, append_to_uri_path as append_to_uri_path

def get_artifact_uri(run_id, artifact_path: Incomplete | None = None, tracking_uri: Incomplete | None = None): ...
