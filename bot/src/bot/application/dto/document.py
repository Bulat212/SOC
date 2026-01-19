from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class AddDocumentNameDTO:
    name: str


@dataclass(slots=True, kw_only=True)
class GetDocumentDTO:
    id: str
    name: str
    url: str


@dataclass(slots=True, kw_only=True)
class GetPromoDocumentDTO(GetDocumentDTO):
    is_active: bool


@dataclass(slots=True, kw_only=True)
class GetDocumentNameDTO:
    name: str


@dataclass(slots=True, kw_only=True)
class GetDocumentsNameDTO:
    values: list[GetDocumentNameDTO]


@dataclass(slots=True, kw_only=True)
class AddDocumentDTO:
    name: str
    file: bytes
    filename: str
    candidate_id: str | None = field(default=None)
