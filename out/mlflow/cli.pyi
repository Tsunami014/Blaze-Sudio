from mlflow import projects as projects, tracking as tracking, version as version
from mlflow.entities import ViewType as ViewType
from mlflow.entities.lifecycle_stage import LifecycleStage as LifecycleStage
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.store.artifact.artifact_repository_registry import get_artifact_repository as get_artifact_repository
from mlflow.store.tracking import DEFAULT_ARTIFACTS_URI as DEFAULT_ARTIFACTS_URI, DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH as DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH
from mlflow.utils import cli_args as cli_args
from mlflow.utils.logging_utils import eprint as eprint
from mlflow.utils.process import ShellCommandException as ShellCommandException
from mlflow.utils.server_cli_utils import artifacts_only_config_validation as artifacts_only_config_validation, resolve_default_artifact_root as resolve_default_artifact_root

def cli() -> None: ...
def run(uri, entry_point, version, param_list, docker_args, experiment_name, experiment_id, backend, backend_config, no_conda, env_manager, storage_dir, run_id, run_name, skip_image_build) -> None: ...
def ui(backend_store_uri, registry_store_uri, default_artifact_root, serve_artifacts, artifacts_destination, port, host) -> None: ...
def server(backend_store_uri, registry_store_uri, default_artifact_root, serve_artifacts, artifacts_only, artifacts_destination, host, port, workers, static_prefix, gunicorn_opts, waitress_opts, expose_prometheus) -> None: ...
def gc(older_than, backend_store_uri, run_ids, experiment_ids) -> None: ...
