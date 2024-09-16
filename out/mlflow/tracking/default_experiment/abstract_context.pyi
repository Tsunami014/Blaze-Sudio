import abc
from abc import ABCMeta, abstractmethod

class DefaultExperimentProvider(metaclass=abc.ABCMeta):
    __metaclass__ = ABCMeta
    @abstractmethod
    def in_context(self): ...
    @abstractmethod
    def get_experiment_id(self): ...
