from _typeshed import Incomplete
from mlflow.entities import Experiment as Experiment, ExperimentTag as ExperimentTag, Metric as Metric, Param as Param, Run as Run, RunData as RunData, RunInfo as RunInfo, RunStatus as RunStatus, RunTag as RunTag, SourceType as SourceType, ViewType as ViewType
from mlflow.entities.lifecycle_stage import LifecycleStage as LifecycleStage
from mlflow.store.db.base_sql_model import Base as Base
from mlflow.utils.time_utils import get_current_time_millis as get_current_time_millis

SourceTypes: Incomplete
RunStatusTypes: Incomplete

class SqlExperiment(Base):
    __tablename__: str
    experiment_id: Incomplete
    name: Incomplete
    artifact_location: Incomplete
    lifecycle_stage: Incomplete
    creation_time: Incomplete
    last_update_time: Incomplete
    __table_args__: Incomplete
    def to_mlflow_entity(self): ...

class SqlRun(Base):
    __tablename__: str
    run_uuid: Incomplete
    name: Incomplete
    source_type: Incomplete
    source_name: Incomplete
    entry_point_name: Incomplete
    user_id: Incomplete
    status: Incomplete
    start_time: Incomplete
    end_time: Incomplete
    deleted_time: Incomplete
    source_version: Incomplete
    lifecycle_stage: Incomplete
    artifact_uri: Incomplete
    experiment_id: Incomplete
    experiment: Incomplete
    __table_args__: Incomplete
    @staticmethod
    def get_attribute_name(mlflow_attribute_name): ...
    def to_mlflow_entity(self): ...

class SqlExperimentTag(Base):
    __tablename__: str
    key: Incomplete
    value: Incomplete
    experiment_id: Incomplete
    experiment: Incomplete
    __table_args__: Incomplete
    def to_mlflow_entity(self): ...

class SqlTag(Base):
    __tablename__: str
    __table_args__: Incomplete
    key: Incomplete
    value: Incomplete
    run_uuid: Incomplete
    run: Incomplete
    def to_mlflow_entity(self): ...

class SqlMetric(Base):
    __tablename__: str
    __table_args__: Incomplete
    key: Incomplete
    value: Incomplete
    timestamp: Incomplete
    step: Incomplete
    is_nan: Incomplete
    run_uuid: Incomplete
    run: Incomplete
    def to_mlflow_entity(self): ...

class SqlLatestMetric(Base):
    __tablename__: str
    __table_args__: Incomplete
    key: Incomplete
    value: Incomplete
    timestamp: Incomplete
    step: Incomplete
    is_nan: Incomplete
    run_uuid: Incomplete
    run: Incomplete
    def to_mlflow_entity(self): ...

class SqlParam(Base):
    __tablename__: str
    __table_args__: Incomplete
    key: Incomplete
    value: Incomplete
    run_uuid: Incomplete
    run: Incomplete
    def to_mlflow_entity(self): ...
