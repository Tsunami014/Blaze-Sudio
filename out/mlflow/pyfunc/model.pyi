import abc
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.models import Model as Model
from mlflow.models.model import MLMODEL_FILE_NAME as MLMODEL_FILE_NAME
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.utils.file_utils import TempDir as TempDir, write_to as write_to

CONFIG_KEY_ARTIFACTS: str
CONFIG_KEY_ARTIFACT_RELATIVE_PATH: str
CONFIG_KEY_ARTIFACT_URI: str
CONFIG_KEY_PYTHON_MODEL: str
CONFIG_KEY_CLOUDPICKLE_VERSION: str

def get_default_pip_requirements(): ...
def get_default_conda_env(): ...

class PythonModel(metaclass=abc.ABCMeta):
    __metaclass__ = ABCMeta
    def load_context(self, context) -> None: ...
    @abstractmethod
    def predict(self, context, model_input): ...

class PythonModelContext:
    def __init__(self, artifacts) -> None: ...
    @property
    def artifacts(self): ...

class _PythonModelPyfuncWrapper:
    python_model: Incomplete
    context: Incomplete
    def __init__(self, python_model, context) -> None: ...
    def predict(self, model_input): ...
