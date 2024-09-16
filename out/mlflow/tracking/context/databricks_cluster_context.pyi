from mlflow.tracking.context.abstract_context import RunContextProvider as RunContextProvider
from mlflow.utils import databricks_utils as databricks_utils
from mlflow.utils.mlflow_tags import MLFLOW_DATABRICKS_CLUSTER_ID as MLFLOW_DATABRICKS_CLUSTER_ID

class DatabricksClusterRunContext(RunContextProvider):
    def in_context(self): ...
    def tags(self): ...
