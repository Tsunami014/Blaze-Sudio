from _typeshed import Incomplete
from mlflow import data as data
from mlflow.exceptions import ExecutionException as ExecutionException
from mlflow.projects import env_type as env_type
from mlflow.tracking import artifact_utils as artifact_utils
from mlflow.utils.file_utils import get_local_path_or_none as get_local_path_or_none
from mlflow.utils.string_utils import is_string_type as is_string_type, quote as quote

MLPROJECT_FILE_NAME: str
DEFAULT_CONDA_FILE_NAME: str

def load_project(directory): ...

class Project:
    env_type: Incomplete
    env_config_path: Incomplete
    docker_env: Incomplete
    name: Incomplete
    def __init__(self, env_type, env_config_path, entry_points, docker_env, name) -> None: ...
    def get_entry_point(self, entry_point): ...

class EntryPoint:
    name: Incomplete
    parameters: Incomplete
    command: Incomplete
    def __init__(self, name, parameters, command) -> None: ...
    def compute_parameters(self, user_parameters, storage_dir): ...
    def compute_command(self, user_parameters, storage_dir): ...

class Parameter:
    name: Incomplete
    type: Incomplete
    default: Incomplete
    def __init__(self, name, yaml_obj) -> None: ...
    def compute_value(self, param_value, storage_dir, key_position): ...
