from _typeshed import Incomplete
from mlflow.store.model_registry.dbmodels.models import SqlModelVersion as SqlModelVersion

revision: str
down_revision: str
branch_labels: Incomplete
depends_on: Incomplete

def upgrade() -> None: ...
def downgrade() -> None: ...
