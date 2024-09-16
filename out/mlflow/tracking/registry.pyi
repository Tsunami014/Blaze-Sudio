import abc
from _typeshed import Incomplete
from abc import ABCMeta, abstractmethod
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.utils.uri import get_uri_scheme as get_uri_scheme

class UnsupportedModelRegistryStoreURIException(MlflowException):
    supported_uri_schemes: Incomplete
    def __init__(self, unsupported_uri, supported_uri_schemes) -> None: ...

class StoreRegistry(metaclass=abc.ABCMeta):
    __metaclass__ = ABCMeta
    group_name: Incomplete
    @abstractmethod
    def __init__(self, group_name): ...
    def register(self, scheme, store_builder) -> None: ...
    def register_entrypoints(self) -> None: ...
    def get_store_builder(self, store_uri): ...
