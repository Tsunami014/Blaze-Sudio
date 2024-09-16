from _typeshed import Incomplete

class SourceType:
    NOTEBOOK: Incomplete
    JOB: Incomplete
    PROJECT: Incomplete
    LOCAL: Incomplete
    UNKNOWN: Incomplete
    PIPELINE: Incomplete
    SOURCETYPE_TO_STRING: Incomplete
    @staticmethod
    def from_string(status_str): ...
    @staticmethod
    def to_string(status): ...
