from _typeshed import Incomplete
from mlflow.entities.model_registry.model_version_stages import STAGE_NONE as STAGE_NONE
from mlflow.entities.model_registry.model_version_status import ModelVersionStatus as ModelVersionStatus
from mlflow.store.model_registry.dbmodels.models import SqlModelVersion as SqlModelVersion, SqlRegisteredModel as SqlRegisteredModel
from sqlalchemy import Boolean as Boolean, Float as Float, and_ as and_, distinct as distinct, func as func

revision: str
down_revision: str
branch_labels: Incomplete
depends_on: Incomplete

def upgrade(): ...
def downgrade() -> None: ...
