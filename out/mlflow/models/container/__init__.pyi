from _typeshed import Incomplete
from mlflow import mleap as mleap, pyfunc as pyfunc
from mlflow.models import Model as Model
from mlflow.models.docker_utils import DISABLE_ENV_CREATION as DISABLE_ENV_CREATION
from mlflow.models.model import MLMODEL_FILE_NAME as MLMODEL_FILE_NAME
from mlflow.pyfunc import mlserver as mlserver, scoring_server as scoring_server

MODEL_PATH: str
DEPLOYMENT_CONFIG_KEY_FLAVOR_NAME: str
DEFAULT_SAGEMAKER_SERVER_PORT: int
DEFAULT_INFERENCE_SERVER_PORT: int
DEFAULT_NGINX_SERVER_PORT: int
DEFAULT_MLSERVER_PORT: int
SUPPORTED_FLAVORS: Incomplete
DISABLE_NGINX: str
ENABLE_MLSERVER: str
SERVING_ENVIRONMENT: str
