from _typeshed import Incomplete
from mlflow import pyfunc as pyfunc
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.models import Model as Model
from mlflow.models.model import MLMODEL_FILE_NAME as MLMODEL_FILE_NAME
from mlflow.models.signature import ModelSignature as ModelSignature
from mlflow.models.utils import ModelInputExample as ModelInputExample
from mlflow.tracking._model_registry import DEFAULT_AWAIT_MAX_SLEEP_SECONDS as DEFAULT_AWAIT_MAX_SLEEP_SECONDS
from mlflow.utils.annotations import experimental as experimental
from mlflow.utils.docstring_utils import LOG_MODEL_PARAM_DOCS as LOG_MODEL_PARAM_DOCS, format_docstring as format_docstring
from mlflow.utils.file_utils import write_to as write_to

FLAVOR_NAME: str
ONNX_EXECUTION_PROVIDERS: Incomplete

def get_default_pip_requirements(): ...
def get_default_conda_env(): ...
def save_model(onnx_model, path, conda_env: Incomplete | None = None, code_paths: Incomplete | None = None, mlflow_model: Incomplete | None = None, signature: ModelSignature = None, input_example: ModelInputExample = None, pip_requirements: Incomplete | None = None, extra_pip_requirements: Incomplete | None = None, onnx_execution_providers: Incomplete | None = None): ...

class _OnnxModelWrapper:
    rt: Incomplete
    inputs: Incomplete
    output_names: Incomplete
    def __init__(self, path, providers: Incomplete | None = None) -> None: ...
    def predict(self, data): ...

def load_model(model_uri, dst_path: Incomplete | None = None): ...
def log_model(onnx_model, artifact_path, conda_env: Incomplete | None = None, code_paths: Incomplete | None = None, registered_model_name: Incomplete | None = None, signature: ModelSignature = None, input_example: ModelInputExample = None, await_registration_for=..., pip_requirements: Incomplete | None = None, extra_pip_requirements: Incomplete | None = None, onnx_execution_providers: Incomplete | None = None): ...
