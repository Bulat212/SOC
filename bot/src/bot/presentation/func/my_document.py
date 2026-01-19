import os

from aiogram.fsm.state import State
from aiogram.types import Message, File
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.document import AddDocumentDTO
from bot.application.usecase.candidate import CandidateUseCase
from bot.presentation.state.my_form import MyDocumentState


@inject
async def set_form(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
        usecase: FromDishka[CandidateUseCase],
) -> None:
    await _set_document(
        message=message,
        message_input=message_input,
        manager=manager,
        usecase=usecase,
        state=MyDocumentState.document_form,
        method="add_or_update_form",
        filename="Лист собеседования",
        text="Лист собеседования удачно отправлен.",
    )


@inject
async def set_approval(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
        usecase: FromDishka[CandidateUseCase],
) -> None:
    await _set_document(
        message=message,
        message_input=message_input,
        manager=manager,
        usecase=usecase,
        state=MyDocumentState.document_approval,
        method="add_or_update_approval",
        filename="Согласие на обработку данных",
        text="Согласие на обработку данных удачно отправлено.",
    )


@inject
async def set_statement(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
        usecase: FromDishka[CandidateUseCase],
) -> None:
    await _set_document(
        message=message,
        message_input=message_input,
        manager=manager,
        usecase=usecase,
        state=MyDocumentState.document_statement,
        method="add_or_update_statement",
        filename="Заявление",
        text="Заявление удачно отправлено.",
        is_image=True,
    )


async def _set_document(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
        usecase: CandidateUseCase,
        state: State,
        method: str,
        filename: str,
        text: str,
        is_image: bool = False,
) -> None:
    if is_image:
        file = getattr(message, "photo", None) or getattr(message, "document", None)
    else:
        file = getattr(message, "document", None)

    if file is None:
        await manager.switch_to(
            state=state,
        )
        return
    try:
        file_info: File = await message.bot.get_file(file_id=file.file_id)
    except AttributeError:
        file_info: File = await message.bot.get_file(file_id=file[0].file_id)
    file_path = file_info.file_path
    file = await message.bot.download_file(
        file_path=file_path,
    )
    file.seek(os.SEEK_SET)
    request = AddDocumentDTO(
        name="NaN",
        filename=f"{filename}." + file_path.split("/")[-1].split(".")[-1],
        file=file.read(),
        candidate_id=manager.start_data.get("user_id"),
    )
    cls_method = getattr(usecase, method)
    await cls_method(request)
    await message.answer(
        text=text,
    )
    await manager.done()
