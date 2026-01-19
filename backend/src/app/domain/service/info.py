from dataclasses import asdict

from app.domain.exception.info import InfoNotFound
from app.domain.model import Info


class InfoService:
    def get_info(self, info: Info | None) -> dict[str, str | bool]:
        if not info:
            raise InfoNotFound()
        data = asdict(info)
        return data

    def get_info_id(self, info: Info | None) -> str:
        if not info:
            raise InfoNotFound()
        return info.id
