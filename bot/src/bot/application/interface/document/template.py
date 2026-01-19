import io
from collections.abc import AsyncIterable
from typing import Any


class ITemplate:
    async def get_template_file(
        self,
        chunks: AsyncIterable[bytes],
    ) -> io.BytesIO: ...

    async def generate_file(
        self,
        file: io.BytesIO,
        context: dict[str, Any],
    ) -> io.BytesIO: ...
