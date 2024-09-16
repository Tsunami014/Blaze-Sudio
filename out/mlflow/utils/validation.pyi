from _typeshed import Incomplete
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.store.db.db_types import DATABASE_ENGINES as DATABASE_ENGINES
from mlflow.utils.string_utils import is_string_type as is_string_type

MAX_PARAMS_TAGS_PER_BATCH: int
MAX_METRICS_PER_BATCH: int
MAX_ENTITIES_PER_BATCH: int
MAX_BATCH_LOG_REQUEST_SIZE: Incomplete
MAX_PARAM_VAL_LENGTH: int
MAX_TAG_VAL_LENGTH: int
MAX_EXPERIMENT_TAG_KEY_LENGTH: int
MAX_EXPERIMENT_TAG_VAL_LENGTH: int
MAX_ENTITY_KEY_LENGTH: int
MAX_MODEL_REGISTRY_TAG_KEY_LENGTH: int
MAX_MODEL_REGISTRY_TAG_VALUE_LENGTH: int
MAX_EXPERIMENTS_LISTED_PER_PAGE: int
PARAM_VALIDATION_MSG: str

def bad_path_message(name): ...
def path_not_unique(name): ...
