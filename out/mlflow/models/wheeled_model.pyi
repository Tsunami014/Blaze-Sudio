from _typeshed import Incomplete
from mlflow import MlflowClient as MlflowClient
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import BAD_REQUEST as BAD_REQUEST
from mlflow.pyfunc.model import MLMODEL_FILE_NAME as MLMODEL_FILE_NAME, Model as Model
from mlflow.store.artifact.utils.models import get_model_name_and_version as get_model_name_and_version
from mlflow.utils.annotations import experimental as experimental
from mlflow.utils.uri import get_databricks_profile_uri_from_artifact_uri as get_databricks_profile_uri_from_artifact_uri

class WheeledModel:
    def __init__(self, model_uri) -> None: ...
    @classmethod
    def log_model(cls, model_uri, registered_model_name: Incomplete | None = None): ...
    def save_model(self, path, mlflow_model: Incomplete | None = None): ...
    @classmethod
    def get_wheel_artifact_path(cls, original_artifact_path): ...
