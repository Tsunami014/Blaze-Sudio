from _typeshed import Incomplete
from mlflow.protos import service_pb2 as service_pb2

class ViewType:
    ACTIVE_ONLY: Incomplete
    DELETED_ONLY: Incomplete
    ALL: Incomplete
    @classmethod
    def from_string(cls, view_str): ...
    @classmethod
    def to_string(cls, view_type): ...
    @classmethod
    def to_proto(cls, view_type): ...
    @classmethod
    def from_proto(cls, proto_view_type): ...
