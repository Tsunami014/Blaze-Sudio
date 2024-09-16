from mlflow.exceptions import MlflowException as MlflowException
from mlflow.store.artifact.http_artifact_repo import HttpArtifactRepository as HttpArtifactRepository
from mlflow.tracking._tracking_service.utils import get_tracking_uri as get_tracking_uri

class MlflowArtifactsRepository(HttpArtifactRepository):
    def __init__(self, artifact_uri) -> None: ...
    @classmethod
    def resolve_uri(cls, artifact_uri, tracking_uri): ...
