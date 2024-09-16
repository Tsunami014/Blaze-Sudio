from _typeshed import Incomplete

class _EnvironmentVariable:
    name: Incomplete
    type: Incomplete
    default: Incomplete
    def __init__(self, name, type_, default) -> None: ...
    @property
    def is_defined(self): ...
    def get(self): ...

class _BooleanEnvironmentVariable(_EnvironmentVariable):
    def __init__(self, name, default) -> None: ...
    def get(self): ...

MLFLOW_DFS_TMP: Incomplete
MLFLOW_HTTP_REQUEST_MAX_RETRIES: Incomplete
MLFLOW_HTTP_REQUEST_BACKOFF_FACTOR: Incomplete
MLFLOW_HTTP_REQUEST_TIMEOUT: Incomplete
MLFLOW_TRACKING_AWS_SIGV4: Incomplete
MLFLOW_GCS_DOWNLOAD_CHUNK_SIZE: Incomplete
MLFLOW_GCS_UPLOAD_CHUNK_SIZE: Incomplete
MLFLOW_GCS_DEFAULT_TIMEOUT: Incomplete
MLFLOW_S3_ENDPOINT_URL: Incomplete
MLFLOW_S3_IGNORE_TLS: Incomplete
MLFLOW_S3_UPLOAD_EXTRA_ARGS: Incomplete
MLFLOW_KERBEROS_TICKET_CACHE: Incomplete
MLFLOW_KERBEROS_USER: Incomplete
MLFLOW_PYARROW_EXTRA_CONF: Incomplete
MLFLOW_SQLALCHEMYSTORE_POOL_SIZE: Incomplete
MLFLOW_SQLALCHEMYSTORE_POOL_RECYCLE: Incomplete
MLFLOW_SQLALCHEMYSTORE_MAX_OVERFLOW: Incomplete
MLFLOW_SQLALCHEMYSTORE_ECHO: Incomplete
MLFLOW_SQLALCHEMYSTORE_POOLCLASS: Incomplete
MLFLOW_REQUIREMENTS_INFERENCE_TIMEOUT: Incomplete
MLFLOW_ALLOW_FILE_URI_AS_MODEL_VERSION_SOURCE: Incomplete
