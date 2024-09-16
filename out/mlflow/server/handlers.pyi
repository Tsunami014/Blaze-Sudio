from _typeshed import Incomplete
from mlflow.entities import ExperimentTag as ExperimentTag, FileInfo as FileInfo, Metric as Metric, Param as Param, RunTag as RunTag, ViewType as ViewType
from mlflow.entities.model_registry import ModelVersionTag as ModelVersionTag, RegisteredModelTag as RegisteredModelTag
from mlflow.environment_variables import MLFLOW_ALLOW_FILE_URI_AS_MODEL_VERSION_SOURCE as MLFLOW_ALLOW_FILE_URI_AS_MODEL_VERSION_SOURCE
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.models import Model as Model
from mlflow.models.model import MLMODEL_FILE_NAME as MLMODEL_FILE_NAME
from mlflow.projects._project_spec import MLPROJECT_FILE_NAME as MLPROJECT_FILE_NAME
from mlflow.protos import databricks_pb2 as databricks_pb2
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE, RESOURCE_DOES_NOT_EXIST as RESOURCE_DOES_NOT_EXIST
from mlflow.protos.mlflow_artifacts_pb2 import DeleteArtifact as DeleteArtifact, DownloadArtifact as DownloadArtifact, MlflowArtifactsService as MlflowArtifactsService, UploadArtifact as UploadArtifact
from mlflow.protos.model_registry_pb2 import CreateModelVersion as CreateModelVersion, CreateRegisteredModel as CreateRegisteredModel, DeleteModelVersion as DeleteModelVersion, DeleteModelVersionTag as DeleteModelVersionTag, DeleteRegisteredModel as DeleteRegisteredModel, DeleteRegisteredModelTag as DeleteRegisteredModelTag, GetLatestVersions as GetLatestVersions, GetModelVersion as GetModelVersion, GetModelVersionDownloadUri as GetModelVersionDownloadUri, GetRegisteredModel as GetRegisteredModel, ListRegisteredModels as ListRegisteredModels, ModelRegistryService as ModelRegistryService, RenameRegisteredModel as RenameRegisteredModel, SearchModelVersions as SearchModelVersions, SearchRegisteredModels as SearchRegisteredModels, SetModelVersionTag as SetModelVersionTag, SetRegisteredModelTag as SetRegisteredModelTag, TransitionModelVersionStage as TransitionModelVersionStage, UpdateModelVersion as UpdateModelVersion, UpdateRegisteredModel as UpdateRegisteredModel
from mlflow.protos.service_pb2 import CreateExperiment as CreateExperiment, CreateRun as CreateRun, DeleteExperiment as DeleteExperiment, DeleteRun as DeleteRun, DeleteTag as DeleteTag, GetExperiment as GetExperiment, GetExperimentByName as GetExperimentByName, GetMetricHistory as GetMetricHistory, GetRun as GetRun, ListArtifacts as ListArtifacts, ListExperiments as ListExperiments, LogBatch as LogBatch, LogMetric as LogMetric, LogModel as LogModel, LogParam as LogParam, MlflowService as MlflowService, RestoreExperiment as RestoreExperiment, RestoreRun as RestoreRun, SearchExperiments as SearchExperiments, SearchRuns as SearchRuns, SetExperimentTag as SetExperimentTag, SetTag as SetTag, UpdateExperiment as UpdateExperiment, UpdateRun as UpdateRun
from mlflow.store.artifact.artifact_repository_registry import get_artifact_repository as get_artifact_repository
from mlflow.store.db.db_types import DATABASE_ENGINES as DATABASE_ENGINES
from mlflow.tracking._model_registry.registry import ModelRegistryStoreRegistry as ModelRegistryStoreRegistry
from mlflow.tracking._tracking_service.registry import TrackingStoreRegistry as TrackingStoreRegistry
from mlflow.tracking.registry import UnsupportedModelRegistryStoreURIException as UnsupportedModelRegistryStoreURIException
from mlflow.utils.file_utils import local_file_uri_to_path as local_file_uri_to_path
from mlflow.utils.proto_json_utils import message_to_json as message_to_json, parse_dict as parse_dict
from mlflow.utils.string_utils import is_string_type as is_string_type
from mlflow.utils.uri import is_file_uri as is_file_uri, is_local_uri as is_local_uri

STATIC_PREFIX_ENV_VAR: str

class TrackingStoreRegistryWrapper(TrackingStoreRegistry):
    def __init__(self) -> None: ...

class ModelRegistryStoreRegistryWrapper(ModelRegistryStoreRegistry):
    def __init__(self) -> None: ...

def initialize_backend_stores(backend_store_uri: Incomplete | None = None, registry_store_uri: Incomplete | None = None, default_artifact_root: Incomplete | None = None) -> None: ...
def catch_mlflow_exception(func): ...
def validate_path_is_safe(path) -> None: ...
def get_artifact_handler(): ...
def get_model_version_artifact_handler(): ...
def get_handler(request_class): ...
def get_endpoints(): ...

HANDLERS: Incomplete
