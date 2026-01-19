from dataclasses import asdict
import datetime

from bot.domain.exception.delegate import DelegateNotFound
from bot.domain.model import Delegate


class DelegateService:
    def get_delegate(self, delegate: Delegate | None) -> dict[str, str | datetime.date]:
        if not delegate:
            raise DelegateNotFound()
        return asdict(delegate)
    
    def add_delegate(self, **data: str | bool | datetime.date) -> Delegate:
        delegate = Delegate(**data)
        return delegate

    def update_delegate(
            self,
            delegate: Delegate,
            **data: str | datetime.date,
    ) -> Delegate:
        data["start_date"] = datetime.datetime.strptime(
            data.get("start_date"),
            "%d.%m.%Y",
        ).isoformat() if data["start_date"] else None
        data["end_date"] = datetime.datetime.strptime(
            data.get("end_date"),
            "%d.%m.%Y",
        ).isoformat() if data["end_date"] else None
        for key, val in data.items():
            if val is None:
                continue
            setattr(delegate, key, val)
        return delegate
