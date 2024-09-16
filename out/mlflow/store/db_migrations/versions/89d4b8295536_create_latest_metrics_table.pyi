from _typeshed import Incomplete
from mlflow.store.tracking.dbmodels.models import SqlLatestMetric as SqlLatestMetric, SqlMetric as SqlMetric

revision: str
down_revision: str
branch_labels: Incomplete
depends_on: Incomplete

def upgrade(): ...
def downgrade() -> None: ...
