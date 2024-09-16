import abc
from _typeshed import Incomplete
from enum import Enum
from mlflow.pipelines.cards import BaseCard as BaseCard, CARD_HTML_NAME as CARD_HTML_NAME, CARD_PICKLE_NAME as CARD_PICKLE_NAME, FailureCard as FailureCard
from mlflow.pipelines.utils import get_pipeline_name as get_pipeline_name
from mlflow.pipelines.utils.step import display_html as display_html
from mlflow.tracking import MlflowClient as MlflowClient
from mlflow.utils.annotations import experimental as experimental
from mlflow.utils.databricks_utils import is_in_databricks_runtime as is_in_databricks_runtime
from typing import Any, TypeVar

class StepStatus(Enum):
    UNKNOWN = 'UNKNOWN'
    RUNNING = 'RUNNING'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'

class StepClass(Enum):
    UNKNOWN = 'UNKNOWN'
    TRAINING = 'TRAINING'
    PREDICTION = 'PREDICTION'
StepExecutionStateType = TypeVar('StepExecutionStateType', bound='StepExecutionState')

class StepExecutionState:
    status: Incomplete
    last_updated_timestamp: Incomplete
    def __init__(self, status: StepStatus, last_updated_timestamp: int) -> None: ...
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, state_dict) -> StepExecutionStateType: ...
StepType = TypeVar('StepType', bound='BaseStep')

class BaseStep(metaclass=abc.ABCMeta):
    step_config: Incomplete
    pipeline_root: Incomplete
    pipeline_name: Incomplete
    step_card: Incomplete
    def __init__(self, step_config: dict[str, Any], pipeline_root: str) -> None: ...
    def run(self, output_directory: str): ...
    def inspect(self, output_directory: str): ...
    @classmethod
    @abc.abstractmethod
    def from_pipeline_config(cls, pipeline_config: dict[str, Any], pipeline_root: str) -> StepType: ...
    @classmethod
    def from_step_config_path(cls, step_config_path: str, pipeline_root: str) -> StepType: ...
    @property
    @abc.abstractmethod
    def name(self) -> str: ...
    @property
    def environment(self) -> dict[str, str]: ...
    def get_artifacts(self) -> list[Any]: ...
    @abc.abstractmethod
    def step_class(self) -> StepClass: ...
    def get_execution_state(self, output_directory: str) -> StepExecutionState: ...
