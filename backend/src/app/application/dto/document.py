from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class AddDocumentNameDTO:
    name: str


@dataclass(slots=True, kw_only=True)
class GetDocumentDTO:
    id: str
    name: str
    url: str
    candidate_id: str | None = field(default=None)


@dataclass(slots=True, kw_only=True)
class GetPromoDocumentDTO:
    id: str
    name: str
    url: str
    is_active: bool


@dataclass(slots=True, kw_only=True)
class GetDocumentNameDTO:
    name: str


@dataclass(slots=True, kw_only=True)
class GetDocumentsNameDTO:
    values: list[AddDocumentNameDTO]


@dataclass(slots=True, kw_only=True)
class AddDocumentDTO:
    name: str
    file: str
    filename: str
    candidate_id: str | None = field(default=None)


@dataclass(slots=True, kw_only=True)
class UpdateDocumentDTO(AddDocumentDTO):
    pass
