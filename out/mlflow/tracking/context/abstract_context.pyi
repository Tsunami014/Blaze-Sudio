import abc
from abc import ABCMeta, abstractmethod

class RunContextProvider(metaclass=abc.ABCMeta):
    __metaclass__ = ABCMeta
    @abstractmethod
    def in_context(self): ...
    @abstractmethod
    def tags(self): ...
