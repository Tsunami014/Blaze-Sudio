from _typeshed import Incomplete
from fastai.callback.core import Callback
from mlflow.fastai import log_model as log_model
from mlflow.utils.autologging_utils import ExceptionSafeClass as ExceptionSafeClass, get_autologging_config as get_autologging_config

class __MlflowFastaiCallback(Callback, metaclass=ExceptionSafeClass):
    remove_on_fetch: Incomplete
    run_before: Incomplete
    run_after: Incomplete
    metrics_logger: Incomplete
    log_models: Incomplete
    is_fine_tune: Incomplete
    freeze_prefix: str
    def __init__(self, metrics_logger, log_models, is_fine_tune: bool = False) -> None: ...
    def after_epoch(self): ...
    def before_fit(self) -> None: ...
    def after_fit(self) -> None: ...
