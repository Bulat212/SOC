import asyncio

from aiogram.types import CallbackQuery, URLInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.document import AddDocumentNameDTO
from bot.application.usecase.promo import PromoUseCase
from bot.constants import CHUNK_SIZE, PROMO_NAMES_DICT
from bot.domain.exception.document import DocumentNotFound
from bot.presentation.state.promo import PromoState

MEDIA = {
    "docx": "answer_document",
    "pdf": "answer_document",
    "mp4": "answer_video",
    "mpeg": "answer_video",
    "mpg": "answer_video",
    "mkv": "answer_video",
    "mov": "answer_video",
    "svg": "answer_document",
    "jpg": "answer_photo",
    "jpeg": "answer_photo",
    "png": "answer_photo",
}


from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.types import URLInputFile

BUCKET_NAME = "promo"
S3_BASE_URL = "http://s3:9000"

@inject
async def send_photo_promo(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[PromoUseCase],
) -> None:
    
    data = dialog_manager.start_data
    promo_list = data.get("promo")
    item_id: str = dialog_manager.item_id  # noqa
    promo_name=promo_list[int(item_id)].get("name")
    png_files_result = []

    promo_names = PROMO_NAMES_DICT.get(promo_name)
    request = AddDocumentNameDTO(
        name=promo_name,
    )

    try:
        document = await usecase.get(request)
    except DocumentNotFound:
        await dialog_manager.switch_to(
            state=PromoState.invalid,
        )
        return
    file = document.url.split("/")[-1]
    callback = MEDIA.get(file.split(".")[-1].lower())
    func = getattr(cq.message, callback)
    if not func:
        await dialog_manager.switch_to(
            state=PromoState.invalid,
        )
        return
    
    if "video" in callback:
        await cq.message.answer(
            text="Видеоролик скоро отправится... Ожидайте...",
        )
        await func(
            URLInputFile(
                url=document.url,
                filename=document.url.split("/")[-1],
                chunk_size=CHUNK_SIZE,
            ),
        )

    #
    else:
        for i, promo in enumerate(promo_names):
            png_files_result.append(
                InputMediaPhoto(
                    media=URLInputFile(
                        f"{S3_BASE_URL}/promo/{promo_name}/{promo}.png"
                    ),
                    caption=f"📁 {promo_name}" if i == 0 else None
                )
            )
        await cq.message.answer_media_group(media=png_files_result)


@inject
async def send_document(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[PromoUseCase],
) -> None:
    data = dialog_manager.start_data
    promo_list = data.get("promo")
    item_id: str = dialog_manager.item_id  # noqa
    role = data.get("role")
    if role == "director":
        dialog_manager.start_data["promo_name"] = (
            promo_list[int(item_id)]
            .get("name")
        )
        await dialog_manager.switch_to(
            state=PromoState.question,
        )
        return

    request = AddDocumentNameDTO(
        name=promo_list[int(item_id)].get("name"),
    )
    try:
        document = await usecase.get(request)
    except DocumentNotFound:
        await dialog_manager.switch_to(
            state=PromoState.invalid,
        )
        return
    file = document.url.split("/")[-1]
    callback = MEDIA.get(file.split(".")[-1].lower())
    func = getattr(cq.message, callback)
    if not func:
        await dialog_manager.switch_to(
            state=PromoState.invalid,
        )
        return
    if "video" in callback:
        await cq.message.answer(
            text="Видеоролик скоро отправится... Ожидайте...",
        )
    await func(
        URLInputFile(
            url=document.url,
            filename=document.url.split("/")[-1],
            chunk_size=CHUNK_SIZE,
        ),
    )


async def add_promo(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=PromoState.adding_name,
    )


@inject
async def send_promo(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[PromoUseCase],
) -> None:
    data = dialog_manager.start_data
    request = AddDocumentNameDTO(
        name=data.get("promo_name"),
    )
    try:
        document = await usecase.get(request)
    except DocumentNotFound:
        await dialog_manager.switch_to(
            state=PromoState.invalid,
        )
        return
    file = document.url.split("/")[-1]
    callback = MEDIA.get(file.split(".")[-1].lower())
    func = getattr(cq.message, callback)
    if not func:
        await dialog_manager.switch_to(
            state=PromoState.invalid,
        )
        return
    if "video" in callback:
        await cq.message.answer(
            text="Видеоролик скоро отправится... Ожидайте...",
        )
    await func(
        URLInputFile(
            url=document.url,
            filename=document.url.split("/")[-1],
            chunk_size=CHUNK_SIZE,
        ),
    )


@inject
async def delete_promo(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[PromoUseCase],
) -> None:
    data = dialog_manager.start_data
    request = AddDocumentNameDTO(
        name=data.get("promo_name"),
    )
    await usecase.delete(request)
    await dialog_manager.switch_to(
        state=PromoState.delete_file,
    )
    asyncio.create_task(dialog_manager.reset_stack())
