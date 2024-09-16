import abc
from abc import ABCMeta, abstractmethod

class RequestHeaderProvider(metaclass=abc.ABCMeta):
    __metaclass__ = ABCMeta
    @abstractmethod
    def in_context(self): ...
    @abstractmethod
    def request_headers(self): ...
