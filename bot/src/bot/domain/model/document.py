from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class Document:
    id: str
    name: str
    url: str


@dataclass(slots=True, kw_only=True)
class PromoDocument:
    id: str
    name: str
    url: str
    is_active: bool


@dataclass(slots=True, kw_only=True)
class DocumentBuff:
    name: str
    file: str
    filename: str
    candidate_id: str | None = field(default=None)
