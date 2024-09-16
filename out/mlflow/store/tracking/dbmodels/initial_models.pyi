from _typeshed import Incomplete

Base: Incomplete
SourceTypes: Incomplete
RunStatusTypes: Incomplete

class SqlExperiment(Base):
    __tablename__: str
    experiment_id: Incomplete
    name: Incomplete
    artifact_location: Incomplete
    lifecycle_stage: Incomplete
    __table_args__: Incomplete

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
    source_version: Incomplete
    lifecycle_stage: Incomplete
    artifact_uri: Incomplete
    experiment_id: Incomplete
    experiment: Incomplete
    __table_args__: Incomplete

class SqlTag(Base):
    __tablename__: str
    key: Incomplete
    value: Incomplete
    run_uuid: Incomplete
    run: Incomplete
    __table_args__: Incomplete

class SqlMetric(Base):
    __tablename__: str
    key: Incomplete
    value: Incomplete
    timestamp: Incomplete
    run_uuid: Incomplete
    run: Incomplete
    __table_args__: Incomplete

class SqlParam(Base):
    __tablename__: str
    key: Incomplete
    value: Incomplete
    run_uuid: Incomplete
    run: Incomplete
    __table_args__: Incomplete
