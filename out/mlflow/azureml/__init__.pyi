from _typeshed import Incomplete
from mlflow import get_registry_uri as get_registry_uri, get_tracking_uri as get_tracking_uri, pyfunc as pyfunc
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.models import Model as Model
from mlflow.models.model import MLMODEL_FILE_NAME as MLMODEL_FILE_NAME
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.utils import get_unique_resource_id as get_unique_resource_id
from mlflow.utils.annotations import deprecated as deprecated
from mlflow.utils.file_utils import TempDir as TempDir

def build_image(model_uri, workspace, image_name: Incomplete | None = None, model_name: Incomplete | None = None, mlflow_home: Incomplete | None = None, description: Incomplete | None = None, tags: Incomplete | None = None, synchronous: bool = True): ...
def deploy(model_uri, workspace, deployment_config: Incomplete | None = None, service_name: Incomplete | None = None, model_name: Incomplete | None = None, tags: Incomplete | None = None, mlflow_home: Incomplete | None = None, synchronous: bool = True): ...

SCORE_SRC: str
