from _typeshed import Incomplete
from mlflow.deployments.base import BaseDeploymentClient as BaseDeploymentClient
from mlflow.deployments.plugin_manager import DeploymentPlugins as DeploymentPlugins
from mlflow.deployments.utils import parse_target_uri as parse_target_uri

plugin_store: Incomplete

def get_deploy_client(target_uri): ...
def run_local(target, name, model_uri, flavor: Incomplete | None = None, config: Incomplete | None = None): ...
