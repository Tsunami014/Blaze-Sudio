from _typeshed import Incomplete
from mlflow.store.tracking.dbmodels.models import SqlExperimentTag as SqlExperimentTag

revision: str
down_revision: str
branch_labels: Incomplete
depends_on: Incomplete

def upgrade() -> None: ...
def downgrade() -> None: ...
