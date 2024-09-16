from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE

LOCAL: str
CONDA: str
VIRTUALENV: str

def validate(env_manager) -> None: ...
