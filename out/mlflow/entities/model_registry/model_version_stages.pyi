from _typeshed import Incomplete
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE

STAGE_NONE: str
STAGE_STAGING: str
STAGE_PRODUCTION: str
STAGE_ARCHIVED: str
STAGE_DELETED_INTERNAL: str
ALL_STAGES: Incomplete
DEFAULT_STAGES_FOR_GET_LATEST_VERSIONS: Incomplete

def get_canonical_stage(stage): ...
