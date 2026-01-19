from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, URLInputFile
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.application.dto.candidate import CandidateDocumentNameDTO
from bot.application.usecase.candidate import CandidateUseCase
from bot.domain.exception.document import DocumentNotFound
from bot.presentation.state.my_form import MyDocumentState


@inject
async def form_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[CandidateUseCase],
) -> None:
    request = CandidateDocumentNameDTO(
        telegram_id=dialog_manager.start_data.get("user_id"),
        name="form",
    )
    await _send_document(
        cq=cq,
        dialog_manager=dialog_manager,
        usecase=usecase,
        state=MyDocumentState.form,
        request=request,
    )


@inject
async def approval_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[CandidateUseCase],
) -> None:
    request = CandidateDocumentNameDTO(
        telegram_id=dialog_manager.start_data.get("user_id"),
        name="approval",
    )
    await _send_document(
        cq=cq,
        dialog_manager=dialog_manager,
        usecase=usecase,
        state=MyDocumentState.approval,
        request=request,
    )


@inject
async def statement_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        usecase: FromDishka[CandidateUseCase],
) -> None:
    request = CandidateDocumentNameDTO(
        telegram_id=dialog_manager.start_data.get("user_id"),
        name="statement",
    )
    await _send_document(
        cq=cq,
        dialog_manager=dialog_manager,
        usecase=usecase,
        state=MyDocumentState.statement,
        request=request,
    )


async def cancel_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    message_id = cq.message.message_id
    chat_id = cq.message.chat.id
    await cq.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id,
    )
    await dialog_manager.done()


async def send_form(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDocumentState.document_form,
    )


async def send_approval(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDocumentState.document_approval,
    )


async def send_statement(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        state=MyDocumentState.document_statement,
    )


async def _send_document(
        cq: CallbackQuery,
        dialog_manager: DialogManager,
        state: State,
        request: CandidateDocumentNameDTO,
        usecase: CandidateUseCase,
) -> None:
    try:
        document = await usecase.get_candidate_document(request)
    except DocumentNotFound:
        data = dialog_manager.start_data
        await dialog_manager.done()
        await dialog_manager.start(
            state=state,
            show_mode=ShowMode.SEND,
            data=data,
        )
        return
    chat_id = cq.message.chat.id
    async with ChatActionSender.upload_document(
            bot=cq.bot,
            chat_id=chat_id,
    ):
        await cq.message.answer_document(
            document=URLInputFile(
                url=document.url,
                filename=document.url.split("/")[-1],
            ),
        )
    data = dialog_manager.start_data
    await dialog_manager.done()
    await dialog_manager.start(
        state=state,
        show_mode=ShowMode.SEND,
        data=data,
    )
