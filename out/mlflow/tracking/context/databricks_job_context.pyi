from mlflow.entities import SourceType as SourceType
from mlflow.tracking.context.abstract_context import RunContextProvider as RunContextProvider
from mlflow.utils import databricks_utils as databricks_utils
from mlflow.utils.mlflow_tags import MLFLOW_DATABRICKS_JOB_ID as MLFLOW_DATABRICKS_JOB_ID, MLFLOW_DATABRICKS_JOB_RUN_ID as MLFLOW_DATABRICKS_JOB_RUN_ID, MLFLOW_DATABRICKS_JOB_TYPE as MLFLOW_DATABRICKS_JOB_TYPE, MLFLOW_DATABRICKS_WEBAPP_URL as MLFLOW_DATABRICKS_WEBAPP_URL, MLFLOW_DATABRICKS_WORKSPACE_ID as MLFLOW_DATABRICKS_WORKSPACE_ID, MLFLOW_DATABRICKS_WORKSPACE_URL as MLFLOW_DATABRICKS_WORKSPACE_URL, MLFLOW_SOURCE_NAME as MLFLOW_SOURCE_NAME, MLFLOW_SOURCE_TYPE as MLFLOW_SOURCE_TYPE

class DatabricksJobRunContext(RunContextProvider):
    def in_context(self): ...
    def tags(self): ...
