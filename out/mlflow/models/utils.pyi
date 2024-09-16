from _typeshed import Incomplete
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.models import Model as Model
from mlflow.store.artifact.utils.models import get_model_name_and_version as get_model_name_and_version
from mlflow.types import DataType as DataType, Schema as Schema, TensorSpec as TensorSpec
from mlflow.types.utils import TensorsNotSupportedException as TensorsNotSupportedException, clean_tensor_type as clean_tensor_type
from mlflow.utils.annotations import experimental as experimental
from mlflow.utils.proto_json_utils import NumpyEncoder as NumpyEncoder, parse_tf_serving_input as parse_tf_serving_input
from mlflow.utils.uri import get_databricks_profile_uri_from_artifact_uri as get_databricks_profile_uri_from_artifact_uri

HAS_SCIPY: bool
ModelInputExample: Incomplete
PyFuncInput: Incomplete
PyFuncOutput: Incomplete

class _Example:
    data: Incomplete
    info: Incomplete
    def __init__(self, input_example: ModelInputExample) -> None: ...
    def save(self, parent_dir_path: str): ...

def plot_lines(data_series, xlabel, ylabel, legend_loc: Incomplete | None = None, line_kwargs: Incomplete | None = None, title: Incomplete | None = None): ...
def validate_schema(data: PyFuncInput, expected_schema: Schema) -> None: ...
def add_libraries_to_model(model_uri, run_id: Incomplete | None = None, registered_model_name: Incomplete | None = None): ...
def get_model_version_from_model_uri(model_uri): ...
