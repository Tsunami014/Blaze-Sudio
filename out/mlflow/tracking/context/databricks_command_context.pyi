from mlflow.tracking.context.abstract_context import RunContextProvider as RunContextProvider
from mlflow.utils import databricks_utils as databricks_utils
from mlflow.utils.mlflow_tags import MLFLOW_DATABRICKS_NOTEBOOK_COMMAND_ID as MLFLOW_DATABRICKS_NOTEBOOK_COMMAND_ID

class DatabricksCommandRunContext(RunContextProvider):
    def in_context(self): ...
    def tags(self): ...
