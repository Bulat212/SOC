from sqlalchemy.util.typing import Protocol
from ulid import ULID


class ULIDGenerator(Protocol):
    def __call__(self) -> ULID: ...
