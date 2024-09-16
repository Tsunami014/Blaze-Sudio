from _typeshed import Incomplete
from mlflow.projects.submitted_run import SubmittedRun as SubmittedRun

__all__ = ['run', 'SubmittedRun']

def run(uri, entry_point: str = 'main', version: Incomplete | None = None, parameters: Incomplete | None = None, docker_args: Incomplete | None = None, experiment_name: Incomplete | None = None, experiment_id: Incomplete | None = None, backend: str = 'local', backend_config: Incomplete | None = None, use_conda: Incomplete | None = None, storage_dir: Incomplete | None = None, synchronous: bool = True, run_id: Incomplete | None = None, run_name: Incomplete | None = None, env_manager: Incomplete | None = None, skip_image_build: bool = False): ...
