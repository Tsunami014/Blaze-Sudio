from _typeshed import Incomplete
from typing import TypeVar

T = TypeVar('T')

class PagedList(list[T]):
    token: Incomplete
    def __init__(self, items: list[T], token) -> None: ...
