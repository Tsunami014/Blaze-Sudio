import abc
from _typeshed import Incomplete
from abc import abstractmethod
from mlflow.artifacts import download_artifacts as download_artifacts
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import BAD_REQUEST as BAD_REQUEST, INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.utils.file_utils import TempDir as TempDir, download_file_using_http_uri as download_file_using_http_uri, get_local_path_or_none as get_local_path_or_none, local_file_uri_to_path as local_file_uri_to_path, read_parquet_as_pandas_df as read_parquet_as_pandas_df, write_pandas_df_as_parquet as write_pandas_df_as_parquet
from typing import Any

class _Dataset(metaclass=abc.ABCMeta):
    dataset_format: Incomplete
    def __init__(self, dataset_format: str) -> None: ...
    @abstractmethod
    def resolve_to_parquet(self, dst_path: str): ...
    @classmethod
    def from_config(cls, dataset_config: dict[str, Any], pipeline_root: str) -> _DatasetType: ...
    @staticmethod
    @abstractmethod
    def handles_format(dataset_format: str) -> bool: ...

class _LocationBasedDataset(_Dataset, metaclass=abc.ABCMeta):
    location: Incomplete
    def __init__(self, location: str | list[str], dataset_format: str, pipeline_root: str) -> None: ...
    @abstractmethod
    def resolve_to_parquet(self, dst_path: str): ...
    @staticmethod
    @abstractmethod
    def handles_format(dataset_format: str) -> bool: ...

class _DownloadThenConvertDataset(_LocationBasedDataset, metaclass=abc.ABCMeta):
    def resolve_to_parquet(self, dst_path: str): ...

class _PandasConvertibleDataset(_DownloadThenConvertDataset, metaclass=abc.ABCMeta):
    @staticmethod
    @abstractmethod
    def handles_format(dataset_format: str) -> bool: ...

class ParquetDataset(_PandasConvertibleDataset):
    @staticmethod
    def handles_format(dataset_format: str) -> bool: ...

class CustomDataset(_PandasConvertibleDataset):
    pipeline_root: Incomplete
    def __init__(self, location: str, dataset_format: str, custom_loader_method: str, pipeline_root: str) -> None: ...
    @staticmethod
    def handles_format(dataset_format: str) -> bool: ...

class _SparkDatasetMixin: ...

class DeltaTableDataset(_SparkDatasetMixin, _LocationBasedDataset):
    version: Incomplete
    timestamp: Incomplete
    def __init__(self, location: str, dataset_format: str, pipeline_root: str, version: int | None = None, timestamp: str | None = None) -> None: ...
    def resolve_to_parquet(self, dst_path: str): ...
    @staticmethod
    def handles_format(dataset_format: str) -> bool: ...

class SparkSqlDataset(_SparkDatasetMixin, _Dataset):
    sql: Incomplete
    location: Incomplete
    def __init__(self, sql: str, location: str, dataset_format: str) -> None: ...
    def resolve_to_parquet(self, dst_path: str): ...
    @staticmethod
    def handles_format(dataset_format: str) -> bool: ...
