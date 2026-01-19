from pydantic import Field

from app.presentation.schema.base import Base


class DocumentNameSchema(Base):
    name: str = Field(...)


class GetDocumentSchema(Base):
    id: str = Field(...)
    name: str = Field(...)
    url: str = Field(...)


class GetDocumentPromoSchema(GetDocumentSchema):
    is_active: bool = Field(...)


class GetDocumentNameSchema(Base):
    name: str = Field(...)


class GetDocumentsNameSchema(Base):
    values: list[GetDocumentNameSchema]


class AddDocumentSchema(Base):
    name: str = Field(...)
    file: str = Field(...)
    filename: str = Field(...)
    candidate_id: str | None = Field(None)


class UpdateDocumentSchema(AddDocumentSchema):
    pass
