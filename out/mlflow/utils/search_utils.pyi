from _typeshed import Incomplete
from mlflow.entities import RunInfo as RunInfo
from mlflow.exceptions import MlflowException as MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE as INVALID_PARAMETER_VALUE
from mlflow.store.db.db_types import MSSQL as MSSQL, MYSQL as MYSQL, POSTGRES as POSTGRES, SQLITE as SQLITE

class SearchUtils:
    LIKE_OPERATOR: str
    ILIKE_OPERATOR: str
    ASC_OPERATOR: str
    DESC_OPERATOR: str
    VALID_ORDER_BY_TAGS: Incomplete
    VALID_METRIC_COMPARATORS: Incomplete
    VALID_PARAM_COMPARATORS: Incomplete
    VALID_TAG_COMPARATORS: Incomplete
    VALID_STRING_ATTRIBUTE_COMPARATORS: Incomplete
    VALID_NUMERIC_ATTRIBUTE_COMPARATORS = VALID_METRIC_COMPARATORS
    NUMERIC_ATTRIBUTES: Incomplete
    VALID_SEARCH_ATTRIBUTE_KEYS: Incomplete
    VALID_ORDER_BY_ATTRIBUTE_KEYS: Incomplete
    STRING_VALUE_TYPES: Incomplete
    DELIMITER_VALUE_TYPES: Incomplete
    WHITESPACE_VALUE_TYPE: Incomplete
    NUMERIC_VALUE_TYPES: Incomplete
    ORDER_BY_KEY_TIMESTAMP: str
    ORDER_BY_KEY_LAST_UPDATED_TIMESTAMP: str
    ORDER_BY_KEY_MODEL_NAME: str
    VALID_ORDER_BY_KEYS_REGISTERED_MODELS: Incomplete
    VALID_TIMESTAMP_ORDER_BY_KEYS: Incomplete
    RECOMMENDED_ORDER_BY_KEYS_REGISTERED_MODELS: Incomplete
    @staticmethod
    def get_comparison_func(comparator): ...
    @staticmethod
    def get_sql_comparison_func(comparator, dialect): ...
    @classmethod
    def parse_search_filter(cls, filter_string): ...
    @classmethod
    def is_metric(cls, key_type, comparator): ...
    @classmethod
    def is_param(cls, key_type, comparator): ...
    @classmethod
    def is_tag(cls, key_type, comparator): ...
    @classmethod
    def is_string_attribute(cls, key_type, key_name, comparator): ...
    @classmethod
    def is_numeric_attribute(cls, key_type, key_name, comparator): ...
    @classmethod
    def filter(cls, runs, filter_string): ...
    @classmethod
    def parse_order_by_for_search_runs(cls, order_by): ...
    @classmethod
    def parse_order_by_for_search_registered_models(cls, order_by): ...
    @classmethod
    def sort(cls, runs, order_by_list): ...
    @classmethod
    def parse_start_offset_from_page_token(cls, page_token): ...
    @classmethod
    def create_page_token(cls, offset): ...
    @classmethod
    def paginate(cls, runs, page_token, max_results): ...
    VALID_SEARCH_KEYS_FOR_MODEL_VERSIONS: Incomplete
    VALID_SEARCH_KEYS_FOR_REGISTERED_MODELS: Incomplete

class SearchExperimentsUtils(SearchUtils):
    VALID_SEARCH_ATTRIBUTE_KEYS: Incomplete
    VALID_ORDER_BY_ATTRIBUTE_KEYS: Incomplete
    NUMERIC_ATTRIBUTES: Incomplete
    @classmethod
    def parse_order_by_for_search_experiments(cls, order_by): ...
    @classmethod
    def is_attribute(cls, key_type, comparator): ...
    @classmethod
    def filter(cls, experiments, filter_string): ...
    @classmethod
    def sort(cls, experiments, order_by_list): ...

class SearchModelUtils(SearchUtils): ...
