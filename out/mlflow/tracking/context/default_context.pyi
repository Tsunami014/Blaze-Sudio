from mlflow.entities import SourceType as SourceType
from mlflow.tracking.context.abstract_context import RunContextProvider as RunContextProvider
from mlflow.utils.mlflow_tags import MLFLOW_SOURCE_NAME as MLFLOW_SOURCE_NAME, MLFLOW_SOURCE_TYPE as MLFLOW_SOURCE_TYPE, MLFLOW_USER as MLFLOW_USER

class DefaultRunContext(RunContextProvider):
    def in_context(self): ...
    def tags(self): ...
