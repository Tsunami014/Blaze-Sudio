from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos import databricks_pb2 as databricks_pb2
from mlflow.tracking.client import MlflowClient as MlflowClient
from mlflow.tracking.default_experiment.abstract_context import DefaultExperimentProvider as DefaultExperimentProvider
from mlflow.utils import databricks_utils as databricks_utils
from mlflow.utils.mlflow_tags import MLFLOW_EXPERIMENT_SOURCE_ID as MLFLOW_EXPERIMENT_SOURCE_ID, MLFLOW_EXPERIMENT_SOURCE_TYPE as MLFLOW_EXPERIMENT_SOURCE_TYPE

class DatabricksNotebookExperimentProvider(DefaultExperimentProvider):
    def in_context(self): ...
    def get_experiment_id(self): ...

class DatabricksRepoNotebookExperimentProvider(DefaultExperimentProvider):
    def in_context(self): ...
    def get_experiment_id(self): ...
