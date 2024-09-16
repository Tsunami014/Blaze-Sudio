from _typeshed import Incomplete
from mlflow.exceptions import ExecutionException as ExecutionException
from mlflow.utils import process as process

MLFLOW_CONDA_HOME: str
MLFLOW_CONDA_CREATE_ENV_CMD: str

def get_conda_command(conda_env_name): ...
def get_conda_bin_executable(executable_name): ...
def get_or_create_conda_env(conda_env_path, env_id: Incomplete | None = None, capture_output: bool = False, env_root_dir: Incomplete | None = None): ...
