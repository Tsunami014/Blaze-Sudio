from _typeshed import Incomplete
from mlflow.server import handlers as handlers
from mlflow.server.handlers import STATIC_PREFIX_ENV_VAR as STATIC_PREFIX_ENV_VAR, get_artifact_handler as get_artifact_handler, get_model_version_artifact_handler as get_model_version_artifact_handler
from mlflow.server.prometheus_exporter import activate_prometheus_exporter as activate_prometheus_exporter

BACKEND_STORE_URI_ENV_VAR: str
REGISTRY_STORE_URI_ENV_VAR: str
ARTIFACT_ROOT_ENV_VAR: str
ARTIFACTS_DESTINATION_ENV_VAR: str
PROMETHEUS_EXPORTER_ENV_VAR: str
SERVE_ARTIFACTS_ENV_VAR: str
ARTIFACTS_ONLY_ENV_VAR: str
REL_STATIC_DIR: str
app: Incomplete
STATIC_DIR: Incomplete
prometheus_metrics_path: Incomplete

def health(): ...
def serve_artifacts(): ...
def serve_model_version_artifact(): ...
def serve_static_file(path): ...
def serve(): ...
