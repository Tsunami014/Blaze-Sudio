from mlflow.exceptions import MlflowException as MlflowException
from mlflow.store.artifact.azure_blob_artifact_repo import AzureBlobArtifactRepository as AzureBlobArtifactRepository
from mlflow.store.artifact.dbfs_artifact_repo import dbfs_artifact_repo_factory as dbfs_artifact_repo_factory
from mlflow.store.artifact.ftp_artifact_repo import FTPArtifactRepository as FTPArtifactRepository
from mlflow.store.artifact.gcs_artifact_repo import GCSArtifactRepository as GCSArtifactRepository
from mlflow.store.artifact.hdfs_artifact_repo import HdfsArtifactRepository as HdfsArtifactRepository
from mlflow.store.artifact.http_artifact_repo import HttpArtifactRepository as HttpArtifactRepository
from mlflow.store.artifact.local_artifact_repo import LocalArtifactRepository as LocalArtifactRepository
from mlflow.store.artifact.mlflow_artifacts_repo import MlflowArtifactsRepository as MlflowArtifactsRepository
from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository as ModelsArtifactRepository
from mlflow.store.artifact.runs_artifact_repo import RunsArtifactRepository as RunsArtifactRepository
from mlflow.store.artifact.s3_artifact_repo import S3ArtifactRepository as S3ArtifactRepository
from mlflow.store.artifact.sftp_artifact_repo import SFTPArtifactRepository as SFTPArtifactRepository
from mlflow.utils.uri import get_uri_scheme as get_uri_scheme

class ArtifactRepositoryRegistry:
    def __init__(self) -> None: ...
    def register(self, scheme, repository) -> None: ...
    def register_entrypoints(self) -> None: ...
    def get_artifact_repository(self, artifact_uri): ...

def get_artifact_repository(artifact_uri): ...
