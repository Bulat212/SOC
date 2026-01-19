from dataclasses import asdict

from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitRouter, RabbitQueue

from app.application.dto.document import (
    AddDocumentNameDTO,
    AddDocumentDTO,
    GetPromoDocumentDTO,
)
from app.application.usecase.document import (
    PromoDocumentUseCase,
    DocumentUseCase,
)
from app.presentation.schema.document import (
    DocumentNameSchema,
    GetDocumentSchema,
    GetDocumentsNameSchema,
    GetDocumentNameSchema,
    AddDocumentSchema,
)

document_router = RabbitRouter()


@document_router.subscriber(
    queue=RabbitQueue(
        name="get_promo_document",
        auto_delete=True,
    ),
)
@inject
async def get_promo_document(
        data: DocumentNameSchema,
        usecase: FromDishka[PromoDocumentUseCase],
) -> GetPromoDocumentDTO:
    request = AddDocumentNameDTO(**data.model_dump())
    document = await usecase.get(request)
    return GetPromoDocumentDTO(**asdict(document))


@document_router.subscriber(
    queue=RabbitQueue(
        name="get_document",
        auto_delete=True,
    ),
)
@inject
async def get_document(
        data: DocumentNameSchema,
        usecase: FromDishka[DocumentUseCase],
) -> GetDocumentSchema:
    request = AddDocumentNameDTO(**data.model_dump())
    document = await usecase.get(request)
    return GetDocumentSchema(**asdict(document))


@document_router.subscriber(
    queue=RabbitQueue(
        name="get_promo_documents_name",
        auto_delete=True,
    ),
)
@inject
async def get_promo_documents_name(
        usecase: FromDishka[PromoDocumentUseCase],
) -> GetDocumentsNameSchema:
    # TODO: Добавить пагинацию
    name_list = await usecase.get_name_all()
    return GetDocumentsNameSchema(
        values=[
            GetDocumentNameSchema(**asdict(val))
            for val in name_list.values
        ],
    )


@document_router.subscriber(
    queue=RabbitQueue(
        name="add_promo_document",
        auto_delete=True,
    ),
)
@inject
async def add_promo_document(
        data: AddDocumentSchema,
        usecase: FromDishka[PromoDocumentUseCase],
) -> GetPromoDocumentDTO:
    request = AddDocumentDTO(**data.model_dump())
    document = await usecase.add(request)
    return GetPromoDocumentDTO(**asdict(document))


@document_router.subscriber(
    queue=RabbitQueue(
        name="delete_promo_document",
        auto_delete=True,
    ),
)
@inject
async def delete_promo_document(
        data: DocumentNameSchema,
        usecase: FromDishka[PromoDocumentUseCase],
) -> None:
    request = AddDocumentNameDTO(**data.model_dump())
    await usecase.delete(request)
