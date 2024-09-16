import abc
from abc import ABCMeta, abstractmethod

class AbstractBackend(metaclass=abc.ABCMeta):
    __metaclass__ = ABCMeta
    @abstractmethod
    def run(self, project_uri, entry_point, params, version, backend_config, tracking_uri, experiment_id): ...
