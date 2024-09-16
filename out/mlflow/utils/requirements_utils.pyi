from _typeshed import Incomplete
from mlflow.environment_variables import MLFLOW_REQUIREMENTS_INFERENCE_TIMEOUT as MLFLOW_REQUIREMENTS_INFERENCE_TIMEOUT
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.utils.databricks_utils import is_in_databricks_runtime as is_in_databricks_runtime
from typing import NamedTuple

class _Requirement(NamedTuple):
    req_str: Incomplete
    is_constraint: Incomplete

DATABRICKS_MODULES_TO_PACKAGES: Incomplete

class _PyPIPackageIndex(NamedTuple):
    date: Incomplete
    package_names: Incomplete

class _MismatchedPackageInfo(NamedTuple):
    package_name: str
    installed_version: str | None
    requirement: str
