from _typeshed import Incomplete
from mlflow.entities import RunStatus as RunStatus, ViewType as ViewType
from mlflow.entities.lifecycle_stage import LifecycleStage as LifecycleStage
from mlflow.store.tracking.dbmodels.models import SourceTypes as SourceTypes, SqlRun as SqlRun

revision: str
down_revision: str
branch_labels: Incomplete
depends_on: Incomplete
old_run_statuses: Incomplete
new_run_statuses: Incomplete
check_constraint_table_args: Incomplete

def upgrade() -> None: ...
def downgrade() -> None: ...
