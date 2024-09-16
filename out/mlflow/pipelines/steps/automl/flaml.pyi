from mlflow import MlflowException as MlflowException
from mlflow.pipelines.utils.metrics import PipelineMetric as PipelineMetric
from sklearn.base import BaseEstimator as BaseEstimator
from typing import Any

def get_estimator_and_best_params(X, y, task: str, step_config: dict[str, Any], pipeline_root: str, evaluation_metrics: dict[str, PipelineMetric], primary_metric: str) -> tuple[BaseEstimator, dict[str, Any]]: ...
