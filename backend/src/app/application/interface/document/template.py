import io
from abc import abstractmethod
from typing import Any, Protocol


class ITemplate(Protocol):
    @abstractmethod
    async def get_docx(
            self,
            template: io.BytesIO,
            context: dict[str, Any],
    ) -> io.BytesIO: ...
