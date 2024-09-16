from _typeshed import Incomplete
from mlflow import MlflowClient as MlflowClient
from mlflow.utils.file_utils import TempDir as TempDir
from mlflow.utils.mlflow_tags import MLFLOW_PARENT_RUN_ID as MLFLOW_PARENT_RUN_ID
from mlflow.utils.time_utils import get_current_time_millis as get_current_time_millis
from typing import NamedTuple

class _SklearnArtifact(NamedTuple):
    name: Incomplete
    function: Incomplete
    arguments: Incomplete
    title: Incomplete

class _SklearnMetric(NamedTuple):
    name: Incomplete
    function: Incomplete
    arguments: Incomplete
