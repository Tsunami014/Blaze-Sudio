import mlflow
import pandas as pd
from _typeshed import Incomplete
from mlflow import MlflowClient as MlflowClient
from mlflow.entities.metric import Metric as Metric
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.models.evaluation.artifacts import CsvEvaluationArtifact as CsvEvaluationArtifact, ImageEvaluationArtifact as ImageEvaluationArtifact, JsonEvaluationArtifact as JsonEvaluationArtifact, NumpyEvaluationArtifact as NumpyEvaluationArtifact
from mlflow.models.evaluation.base import EvaluationResult as EvaluationResult, ModelEvaluator as ModelEvaluator
from mlflow.models.utils import plot_lines as plot_lines
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.utils.file_utils import TempDir as TempDir
from mlflow.utils.proto_json_utils import NumpyEncoder as NumpyEncoder
from mlflow.utils.time_utils import get_current_time_millis as get_current_time_millis
from typing import Callable, NamedTuple

class _Curve(NamedTuple):
    plot_fn: Incomplete
    plot_fn_args: Incomplete
    auc: Incomplete

class _CustomMetric(NamedTuple):
    function: Callable
    name: str
    index: int
    artifacts_dir: str

class DefaultEvaluator(ModelEvaluator):
    def can_evaluate(self, *, model_type, evaluator_config, **kwargs): ...
    dataset: Incomplete
    run_id: Incomplete
    model_type: Incomplete
    evaluator_config: Incomplete
    dataset_name: Incomplete
    feature_names: Incomplete
    custom_metrics: Incomplete
    y: Incomplete
    pos_label: Incomplete
    sample_weights: Incomplete
    def evaluate(self, *, model: mlflow.pyfunc.PyFuncModel, model_type, dataset, run_id, evaluator_config, custom_metrics: Incomplete | None = None, baseline_model: Incomplete | None = None, **kwargs): ...
    @property
    def X(self) -> pd.DataFrame: ...
    class _MutationGuardedData:
        def __init__(self, data) -> None: ...
        def copy_to_avoid_mutation(self): ...
        def get_original(self): ...
