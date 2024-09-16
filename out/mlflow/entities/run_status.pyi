from _typeshed import Incomplete

class RunStatus:
    RUNNING: Incomplete
    SCHEDULED: Incomplete
    FINISHED: Incomplete
    FAILED: Incomplete
    KILLED: Incomplete
    @staticmethod
    def from_string(status_str): ...
    @staticmethod
    def to_string(status): ...
    @staticmethod
    def is_terminated(status): ...
    @staticmethod
    def all_status(): ...
