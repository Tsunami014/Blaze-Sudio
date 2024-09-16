from _typeshed import Incomplete
from mlflow.tracking.context.databricks_cluster_context import DatabricksClusterRunContext as DatabricksClusterRunContext
from mlflow.tracking.context.databricks_command_context import DatabricksCommandRunContext as DatabricksCommandRunContext
from mlflow.tracking.context.databricks_job_context import DatabricksJobRunContext as DatabricksJobRunContext
from mlflow.tracking.context.databricks_notebook_context import DatabricksNotebookRunContext as DatabricksNotebookRunContext
from mlflow.tracking.context.databricks_repo_context import DatabricksRepoRunContext as DatabricksRepoRunContext
from mlflow.tracking.context.default_context import DefaultRunContext as DefaultRunContext
from mlflow.tracking.context.git_context import GitRunContext as GitRunContext
from mlflow.tracking.context.system_environment_context import SystemEnvironmentContext as SystemEnvironmentContext

class RunContextProviderRegistry:
    def __init__(self) -> None: ...
    def register(self, run_context_provider_cls) -> None: ...
    def register_entrypoints(self) -> None: ...
    def __iter__(self): ...

def resolve_tags(tags: Incomplete | None = None): ...
