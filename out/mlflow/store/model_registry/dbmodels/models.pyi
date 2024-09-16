from _typeshed import Incomplete
from mlflow.entities.model_registry import ModelVersion as ModelVersion, ModelVersionTag as ModelVersionTag, RegisteredModel as RegisteredModel, RegisteredModelTag as RegisteredModelTag
from mlflow.entities.model_registry.model_version_stages import STAGE_DELETED_INTERNAL as STAGE_DELETED_INTERNAL, STAGE_NONE as STAGE_NONE
from mlflow.entities.model_registry.model_version_status import ModelVersionStatus as ModelVersionStatus
from mlflow.store.db.base_sql_model import Base as Base
from mlflow.utils.time_utils import get_current_time_millis as get_current_time_millis

class SqlRegisteredModel(Base):
    __tablename__: str
    name: Incomplete
    creation_time: Incomplete
    last_updated_time: Incomplete
    description: Incomplete
    __table_args__: Incomplete
    def to_mlflow_entity(self): ...

class SqlModelVersion(Base):
    __tablename__: str
    name: Incomplete
    version: Incomplete
    creation_time: Incomplete
    last_updated_time: Incomplete
    description: Incomplete
    user_id: Incomplete
    current_stage: Incomplete
    source: Incomplete
    run_id: Incomplete
    run_link: Incomplete
    status: Incomplete
    status_message: Incomplete
    registered_model: Incomplete
    __table_args__: Incomplete
    def to_mlflow_entity(self): ...

class SqlRegisteredModelTag(Base):
    __tablename__: str
    name: Incomplete
    key: Incomplete
    value: Incomplete
    registered_model: Incomplete
    __table_args__: Incomplete
    def to_mlflow_entity(self): ...

class SqlModelVersionTag(Base):
    __tablename__: str
    name: Incomplete
    version: Incomplete
    key: Incomplete
    value: Incomplete
    model_version: Incomplete
    __table_args__: Incomplete
    def to_mlflow_entity(self): ...
