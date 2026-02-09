from dataclasses import asdict

from dishka.integrations.faststream import FromDishka, inject
from faststream.rabbit import RabbitQueue, RabbitRouter

from app.application.dto.candidate import (
    AddCandidateDTO,
    AddCandidateIDDTO,
    FormDataDTO,
    UpdateCandidateDTO,
    CandidateDocumentNameDTO,
)
from app.application.dto.document import UpdateDocumentDTO
from app.application.usecase.candidate import CandidateUseCase
from app.presentation.schema.candidate import (
    AddCandidateSchema,
    DeleteCandidateSchema,
    FormDataSchema,
    GetCandidateSchema,
    AddCandidateIDSchema,
    UpdateCandidateSchema,
    CandidateDocumentNameSchema,
)
from app.presentation.schema.document import (
    GetDocumentSchema, UpdateDocumentSchema,
)
from app.application.dto.pagination import GetCandidatesByRecruitmentDTO

candidate_router = RabbitRouter()


@candidate_router.subscriber(
    queue=RabbitQueue(
        "add_candidate",
        auto_delete=True,
    ),
)
@inject
async def add_candidate(
        data: AddCandidateSchema,
        usecase: FromDishka[CandidateUseCase],
) -> GetCandidateSchema:
    request = AddCandidateDTO(**data.model_dump())
    candidate = await usecase.add(request)
    return GetCandidateSchema(**asdict(candidate))


@candidate_router.subscriber(
    queue=RabbitQueue(
        "get_candidate",
        auto_delete=True,
    ),
)
@inject
async def get_candidate(
        data: AddCandidateIDSchema,
        usecase: FromDishka[CandidateUseCase],
) -> GetCandidateSchema:
    request = AddCandidateIDDTO(
        id=data.id,
        telegram_id=data.telegram_id,
    )
    candidate = await usecase.get(request)
    return GetCandidateSchema(**asdict(candidate))


@candidate_router.subscriber("get_candidates_by_recruitment")
@inject
async def get_by_recruitment(
    data: GetCandidatesByRecruitmentDTO,
    usecase:  FromDishka[CandidateUseCase],
):
    candidates = await usecase.get_by_recruitment_id(
        recruitment_id=data.recruitment_id,
        limit=data.limit,
        offset=data.offset,
    )
    return candidates


# @candidate_router.subscriber(
#     queue=RabbitQueue(
#         "update_candidate",
#         auto_delete=True,
#     ),
# )
@candidate_router.subscriber("update_candidate")
@inject
async def update_candidate(
        data: UpdateCandidateSchema,
        usecase: FromDishka[CandidateUseCase],
) -> GetCandidateSchema:
    request = UpdateCandidateDTO(**data.model_dump())
    candidate = await usecase.update(request)
    return GetCandidateSchema(**asdict(candidate))


@candidate_router.subscriber(
    queue=RabbitQueue(
        "get_candidate_document",
        auto_delete=True,
    ),
)
@inject
async def get_candidate_document(
        data: CandidateDocumentNameSchema,
        usecase: FromDishka[CandidateUseCase],
) -> GetDocumentSchema:
    request = CandidateDocumentNameDTO(**data.model_dump())
    document = await usecase.get_candidate_document(request)
    return GetDocumentSchema(**asdict(document))


@candidate_router.subscriber(
    queue=RabbitQueue(
        "add_or_update_form",
        auto_delete=True,
    ),
)
@inject
async def add_or_update_form(
        data: UpdateDocumentSchema,
        usecase: FromDishka[CandidateUseCase],
) -> GetDocumentSchema:
    request = UpdateDocumentDTO(**data.model_dump())
    document = await usecase.add_or_update_form(request)
    return GetDocumentSchema(**asdict(document))


@candidate_router.subscriber(
    queue=RabbitQueue(
        "add_or_update_approval",
        auto_delete=True,
    ),
)
@inject
async def add_or_update_approval(
        data: UpdateDocumentSchema,
        usecase: FromDishka[CandidateUseCase],
) -> GetDocumentSchema:
    request = UpdateDocumentDTO(**data.model_dump())
    document = await usecase.add_or_update_approval(request)
    return GetDocumentSchema(**asdict(document))


@candidate_router.subscriber(
    queue=RabbitQueue(
        "add_or_update_statement",
        auto_delete=True,
    ),
)
@inject
async def add_or_update_statement(
        data: UpdateDocumentSchema,
        usecase: FromDishka[CandidateUseCase],
) -> GetDocumentSchema:
    request = UpdateDocumentDTO(**data.model_dump())
    document = await usecase.add_or_update_statement(request)
    return GetDocumentSchema(**asdict(document))


@candidate_router.subscriber(
    queue=RabbitQueue(
        "delete_candidate",
        auto_delete=True,
    ),
)
@inject
async def delete_candidate(
        data: DeleteCandidateSchema,
        usecase: FromDishka[CandidateUseCase],
):
    candidate_id = data.candidate_id
    await usecase.delete_candidate(candidate_id)


@candidate_router.subscriber(
    queue=RabbitQueue(
        "update_candidate_from_yandex",
        auto_delete=True,
    ),
)
@inject
async def update_form_from_yandex(
    data: FormDataSchema,
    usecase: FromDishka[CandidateUseCase],
):
    request = FormDataDTO(**data.model_dump())
    await usecase.update_for_form(request)
    await usecase.add_candidate_from_form(request)
