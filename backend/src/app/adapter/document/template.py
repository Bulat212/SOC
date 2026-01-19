import asyncio
import io
import os
from typing import Any

from docxtpl import DocxTemplate


class Template:
    async def get_docx(
            self,
            template: io.BytesIO,
            context: dict[str, Any],
    ) -> io.BytesIO:
        template.seek(os.SEEK_SET)
        doc = DocxTemplate(template)
        func = await asyncio.to_thread(
            self._generate_file,
            document=doc,
            context=context,
        )
        return func

    def _generate_file(
            self,
            document: DocxTemplate,
            context: dict[str, Any],
    ) -> io.BytesIO:
        buffer = io.BytesIO()
        document.render(context)
        document.save(buffer)
        buffer.seek(os.SEEK_SET)
        return buffer
