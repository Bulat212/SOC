from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class Document:
    id: str | None = field(default=None)
    name: str
    url: str
    info_id: str


@dataclass(slots=True, kw_only=True)
class PromoDocument:
    id: str | None = field(default=None)
    name: str
    url: str
    info_id: str
    is_active: bool = field(default=True)
