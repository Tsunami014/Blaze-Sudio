from mlflow.entities.view_type import ViewType as ViewType
from mlflow.exceptions import MlflowException as MlflowException

class LifecycleStage:
    ACTIVE: str
    DELETED: str
    @classmethod
    def view_type_to_stages(cls, view_type=...): ...
    @classmethod
    def is_valid(cls, lifecycle_stage): ...
    @classmethod
    def matches_view_type(cls, view_type, lifecycle_stage): ...
