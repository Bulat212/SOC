import asyncio

from aiogram.types import CallbackQuery, URLInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.document import AddDocumentNameDTO
from bot.application.usecase.document import DocumentUseCase
from bot.domain.exception.document import DocumentNotFound
from bot.presentation.state.document import (
    DocumentState,
)


@inject
async def send_document(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[DocumentUseCase],
) -> None:
    text: Const = button.text  # noqa
    request = AddDocumentNameDTO(
        name=text.text,
    )
    try:
        document = await usecase.get(request)
    except DocumentNotFound:
        await dialog_manager.switch_to(
            state=DocumentState.invalid,
        )
        asyncio.create_task(dialog_manager.reset_stack())
        return
    await cq.message.answer_document(
        document=URLInputFile(
            url=document.url,
            filename=document.url.split("/")[-1],
        ),
    )


@inject
async def send_image(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[DocumentUseCase],
) -> None:
    text: Const = button.text  # noqa
    request = AddDocumentNameDTO(
        name=text.text,
    )
    try:
        document = await usecase.get(request)
    except DocumentNotFound:
        await dialog_manager.switch_to(
            state=DocumentState.invalid,
        )
        asyncio.create_task(dialog_manager.reset_stack())
        return
    await cq.message.answer_photo(
        photo=URLInputFile(
            url=document.url,
            filename=document.url.split("/")[-1],
        ),
    )
