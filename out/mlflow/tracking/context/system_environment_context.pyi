from mlflow.tracking.context.abstract_context import RunContextProvider as RunContextProvider

MLFLOW_RUN_CONTEXT_ENV_VAR: str

class SystemEnvironmentContext(RunContextProvider):
    def in_context(self): ...
    def tags(self): ...
