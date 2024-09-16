from _typeshed import Incomplete
from mlflow.utils.mlflow_tags import MLFLOW_USER as MLFLOW_USER

revision: str
down_revision: str
branch_labels: Incomplete
depends_on: Incomplete
Base: Incomplete

class SqlRun(Base):
    __tablename__: str
    run_uuid: Incomplete
    user_id: Incomplete
    experiment_id: Incomplete
    __table_args__: Incomplete

class SqlTag(Base):
    __tablename__: str
    key: Incomplete
    value: Incomplete
    run_uuid: Incomplete
    run: Incomplete
    __table_args__: Incomplete

def upgrade() -> None: ...
def downgrade() -> None: ...
