import abc
from abc import abstractmethod
from mlflow.entities._mlflow_object import _MLflowObject

class _ModelRegistryEntity(_MLflowObject, metaclass=abc.ABCMeta):
    @classmethod
    @abstractmethod
    def from_proto(cls, proto): ...
    def __eq__(self, other): ...
