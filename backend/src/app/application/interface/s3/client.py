import io
from abc import abstractmethod
from collections.abc import AsyncIterable
from typing import Protocol


class IMinIOClient(Protocol):
    @abstractmethod
    async def get_object(
            self,
            bucket: str,
            key: str,
    ) -> AsyncIterable[bytes]: ...

    @abstractmethod
    async def put_object(
            self,
            bucket: str,
            key: str,
            file: io.BytesIO | str | bytes,
    ) -> None: ...

    @abstractmethod
    async def delete_object(
            self,
            bucket: str,
            key: str,
    ) -> None: ...

    @abstractmethod
    async def copy_object(
            self,
            bucket: str,
            old_key: str,
            new_key: str,
    ) -> None: ...
