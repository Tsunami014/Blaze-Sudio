from _typeshed import Incomplete
from mlflow import pyfunc as pyfunc
from mlflow.entities import Metric as Metric
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.models import Model as Model, infer_signature as infer_signature
from mlflow.models.model import MLMODEL_FILE_NAME as MLMODEL_FILE_NAME
from mlflow.models.signature import ModelSignature as ModelSignature
from mlflow.models.utils import ModelInputExample as ModelInputExample
from mlflow.tracking._model_registry import DEFAULT_AWAIT_MAX_SLEEP_SECONDS as DEFAULT_AWAIT_MAX_SLEEP_SECONDS
from mlflow.tracking.artifact_utils import get_artifact_uri as get_artifact_uri
from mlflow.tracking.client import MlflowClient as MlflowClient
from mlflow.utils import is_iterator as is_iterator
from mlflow.utils.annotations import keyword_only as keyword_only
from mlflow.utils.autologging_utils import AUTOLOGGING_CONF_KEY_IS_GLOBALLY_CONFIGURED as AUTOLOGGING_CONF_KEY_IS_GLOBALLY_CONFIGURED, PatchFunction as PatchFunction, autologging_integration as autologging_integration, batch_metrics_logger as batch_metrics_logger, get_autologging_config as get_autologging_config, log_fn_args_as_params as log_fn_args_as_params, picklable_exception_safe_function as picklable_exception_safe_function, resolve_input_example_and_signature as resolve_input_example_and_signature, safe_patch as safe_patch
from mlflow.utils.docstring_utils import LOG_MODEL_PARAM_DOCS as LOG_MODEL_PARAM_DOCS, format_docstring as format_docstring
from mlflow.utils.file_utils import TempDir as TempDir, write_to as write_to
from mlflow.utils.time_utils import get_current_time_millis as get_current_time_millis
from typing import NamedTuple

FLAVOR_NAME: str

def get_default_pip_requirements(): ...
def get_default_conda_env(): ...
def log_model(tf_saved_model_dir, tf_meta_graph_tags, tf_signature_def_key, artifact_path, conda_env: Incomplete | None = None, code_paths: Incomplete | None = None, signature: ModelSignature = None, input_example: ModelInputExample = None, registered_model_name: Incomplete | None = None, await_registration_for=..., pip_requirements: Incomplete | None = None, extra_pip_requirements: Incomplete | None = None): ...
def save_model(tf_saved_model_dir, tf_meta_graph_tags, tf_signature_def_key, path, mlflow_model: Incomplete | None = None, conda_env: Incomplete | None = None, code_paths: Incomplete | None = None, signature: ModelSignature = None, input_example: ModelInputExample = None, pip_requirements: Incomplete | None = None, extra_pip_requirements: Incomplete | None = None): ...
def load_model(model_uri, dst_path: Incomplete | None = None): ...

class _TF2Wrapper:
    model: Incomplete
    infer: Incomplete
    def __init__(self, model, infer) -> None: ...
    def predict(self, data): ...

class _TensorBoardLogDir(NamedTuple):
    location: Incomplete
    is_temp: Incomplete

def autolog(every_n_iter: int = 1, log_models: bool = True, disable: bool = False, exclusive: bool = False, disable_for_unsupported_versions: bool = False, silent: bool = False, registered_model_name: Incomplete | None = None, log_input_examples: bool = False, log_model_signatures: bool = False): ...
