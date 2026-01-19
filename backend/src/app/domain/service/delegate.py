from dataclasses import asdict, fields
import datetime

from app.domain.exception.delegate import DelegateNotFound
from app.domain.model import Delegate


class DelegateService:
    def get_delegate(self, delegate: Delegate | None) -> Delegate:
        if not delegate:
            raise DelegateNotFound()
        return delegate
    

    def get_delegate_as_dict(self, delegate: Delegate | None) -> dict[str, str | datetime.date]:
        if not delegate:
            raise DelegateNotFound()
        return asdict(delegate)
    

    def update_delegate(
            self,
            delegate: Delegate | None,
            **data: str | datetime.date | None,
    ) -> Delegate:
        if delegate is None:
            raise DelegateNotFound()

        for key, val in data.items():
            if val is None:
                continue
            setattr(delegate, key, val)

        return delegate
    

    def add_delegate(
            self,
            **data: str | bool | datetime.date | None,
    ) -> Delegate:
        context = dict()
        for val in fields(Delegate):
            context[val.name] = data.get(val.name)

        delegate = Delegate(**context)
        return delegate