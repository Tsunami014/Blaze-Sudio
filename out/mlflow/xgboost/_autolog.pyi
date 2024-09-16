import xgboost
from _typeshed import Incomplete
from mlflow.utils.autologging_utils import ExceptionSafeAbstractClass as ExceptionSafeAbstractClass

def autolog_callback(env, metrics_logger, eval_results) -> None: ...

IS_TRAINING_CALLBACK_SUPPORTED: Incomplete

class AutologCallback(xgboost.callback.TrainingCallback, metaclass=ExceptionSafeAbstractClass):
    metrics_logger: Incomplete
    eval_results: Incomplete
    def __init__(self, metrics_logger, eval_results) -> None: ...
    def after_iteration(self, model, epoch, evals_log): ...
