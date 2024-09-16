from mlflow.entities.model_registry import ModelVersion as ModelVersion
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import ErrorCode as ErrorCode, RESOURCE_ALREADY_EXISTS as RESOURCE_ALREADY_EXISTS
from mlflow.store.artifact.runs_artifact_repo import RunsArtifactRepository as RunsArtifactRepository
from mlflow.tracking._model_registry import DEFAULT_AWAIT_MAX_SLEEP_SECONDS as DEFAULT_AWAIT_MAX_SLEEP_SECONDS
from mlflow.tracking.client import MlflowClient as MlflowClient
from mlflow.utils.logging_utils import eprint as eprint
from typing import Any

def register_model(model_uri, name, await_registration_for=..., *, tags: dict[str, Any] | None = None) -> ModelVersion: ...
