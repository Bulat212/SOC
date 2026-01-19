from dataclasses import asdict

from bot.domain.exception.status import StatusNotFound
from bot.domain.model.status import Status


class StatusService:
    def get_status(self, status: Status | None) -> dict[str, str]:
        if not status:
            raise StatusNotFound()
        data = asdict(status)
        return data
