from mlflow.pipelines.pipeline import _BasePipeline
from mlflow.pipelines.step import BaseStep as BaseStep
from mlflow.pipelines.steps.evaluate import EvaluateStep as EvaluateStep
from mlflow.pipelines.steps.ingest import IngestScoringStep as IngestScoringStep, IngestStep as IngestStep
from mlflow.pipelines.steps.predict import PredictStep as PredictStep
from mlflow.pipelines.steps.register import RegisterStep as RegisterStep
from mlflow.pipelines.steps.split import SplitStep as SplitStep
from mlflow.pipelines.steps.train import TrainStep as TrainStep
from mlflow.pipelines.steps.transform import TransformStep as TransformStep
from mlflow.utils.annotations import experimental as experimental
from typing import Any

class RegressionPipeline(_BasePipeline):
    def run(self, step: str = None) -> None: ...
    def get_artifact(self, artifact_name: str) -> Any | None: ...
    def clean(self, step: str = None) -> None: ...
    def inspect(self, step: str = None) -> None: ...
