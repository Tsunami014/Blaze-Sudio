from _typeshed import Incomplete
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.models import Model as Model
from mlflow.models.model import MLMODEL_FILE_NAME as MLMODEL_FILE_NAME
from mlflow.models.signature import ModelSignature as ModelSignature
from mlflow.models.utils import ModelInputExample as ModelInputExample
from mlflow.utils import reraise as reraise
from mlflow.utils.annotations import keyword_only as keyword_only

FLAVOR_NAME: str

def log_model(spark_model, sample_input, artifact_path, registered_model_name: Incomplete | None = None, signature: ModelSignature = None, input_example: ModelInputExample = None): ...
def save_model(spark_model, sample_input, path, mlflow_model: Incomplete | None = None, signature: ModelSignature = None, input_example: ModelInputExample = None): ...
def add_to_model(mlflow_model, path, spark_model, sample_input) -> None: ...

class MLeapSerializationException(MlflowException): ...
