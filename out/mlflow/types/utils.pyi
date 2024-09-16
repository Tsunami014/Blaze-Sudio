import numpy as np
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.types import DataType as DataType
from mlflow.types.schema import ColSpec as ColSpec, Schema as Schema, TensorSpec as TensorSpec

class TensorsNotSupportedException(MlflowException):
    def __init__(self, msg) -> None: ...

def clean_tensor_type(dtype: np.dtype): ...
