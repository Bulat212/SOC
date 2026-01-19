from dataclasses import asdict

from app.domain.exception.status import StatusNotFound
from app.domain.model import Status
from app.domain.model.status import StatusEnum


class StatusService:
    def add_status(self, **data: str) -> Status:
        data["status"] = StatusEnum.UNDER_REVIEW
        return Status(**data)

    def get_status(self, status: Status) -> dict[str, str]:
        if not status:
            raise StatusNotFound()
        data = asdict(status)
        data["status"] = status.status.value
        return data
