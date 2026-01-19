from dataclasses import asdict

from bot.domain.exception.info import InfoNotFound
from bot.domain.model.info import Info


class InfoService:
    def get_info(self, info: Info | None) -> dict[str, str | bool]:
        if not info:
            raise InfoNotFound()
        data = asdict(info)
        return data
