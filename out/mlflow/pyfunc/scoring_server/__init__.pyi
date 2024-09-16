from _typeshed import Incomplete
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import BAD_REQUEST as BAD_REQUEST
from mlflow.pyfunc import PyFuncModel as PyFuncModel, load_pyfunc as load_model
from mlflow.server.handlers import catch_mlflow_exception as catch_mlflow_exception
from mlflow.types import Schema as Schema
from mlflow.utils import reraise as reraise
from mlflow.utils.file_utils import path_to_local_file_uri as path_to_local_file_uri
from mlflow.utils.proto_json_utils import NumpyEncoder as NumpyEncoder, parse_tf_serving_input as parse_tf_serving_input
from mlflow.version import VERSION as VERSION

CONTENT_TYPE_CSV: str
CONTENT_TYPE_JSON: str
CONTENT_TYPE_JSON_RECORDS_ORIENTED: str
CONTENT_TYPE_JSON_SPLIT_ORIENTED: str
CONTENT_TYPE_JSON_SPLIT_NUMPY: str
CONTENT_TYPES: Incomplete
CONTENT_TYPE_FORMAT_RECORDS_ORIENTED: str
CONTENT_TYPE_FORMAT_SPLIT_ORIENTED: str
FORMATS: Incomplete
PREDICTIONS_WRAPPER_ATTR_NAME_ENV_KEY: str

def infer_and_parse_json_input(json_input, schema: Schema = None): ...
def parse_json_input(json_input, orient: str = 'split', schema: Schema = None): ...
def parse_csv_input(csv_input, schema: Schema = None): ...
def parse_split_oriented_json_input_to_numpy(json_input): ...
def predictions_to_json(raw_predictions, output) -> None: ...
def init(model: PyFuncModel): ...
def get_cmd(model_uri: str, port: int = None, host: int = None, timeout: int = None, nworkers: int = None) -> tuple[str, dict[str, str]]: ...
