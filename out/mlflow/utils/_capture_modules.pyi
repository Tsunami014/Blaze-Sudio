from _typeshed import Incomplete
from mlflow.models.model import MLMODEL_FILE_NAME as MLMODEL_FILE_NAME, Model as Model
from mlflow.pyfunc import MAIN as MAIN
from mlflow.utils.databricks_utils import is_in_databricks_runtime as is_in_databricks_runtime
from mlflow.utils.file_utils import write_to as write_to
from mlflow.utils.requirements_utils import DATABRICKS_MODULES_TO_PACKAGES as DATABRICKS_MODULES_TO_PACKAGES

class _CaptureImportedModules:
    imported_modules: Incomplete
    original_import: Incomplete
    original_import_module: Incomplete
    def __init__(self) -> None: ...
    def __enter__(self): ...
    def __exit__(self, *_, **__) -> None: ...

def parse_args(): ...
def main(): ...
