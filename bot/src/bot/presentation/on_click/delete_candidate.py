from aiogram.types import CallbackQuery, MenuButtonDefault, ReplyKeyboardRemove
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from bot.application.dto.candidate import CandidateIDDTO
from bot.application.dto.user import UserIDDTO
from bot.application.usecase.candidate import CandidateUseCase
from bot.application.usecase.user import UserUseCase
from bot.domain.exception.user import UserNotFound
from bot.presentation.button.start_button import StartCandidateKeyboardButton
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject



async def cancel_delete_click(
        cq: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.done()
    user_id = cq.from_user.id
    keyboard = StartCandidateKeyboardButton(
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    await cq.bot.send_message(
        chat_id=user_id,
        text="Выберите интересующий вас раздел.",
        reply_markup=keyboard(),
    )

@inject
async def confirm_delete(
    cq: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    usecase_user: FromDishka[UserUseCase],
    usecase_candidate: FromDishka[CandidateUseCase],
    **kwargs,
):
    telegram_id = str(cq.from_user.id)

    request = UserIDDTO(telegram_id=telegram_id)

    try:
        user = await usecase_user.get(request)
    except UserNotFound:
        await cq.message.answer("❗ Вы не зарегистрированы как кандидат.")
        await dialog_manager.done()
        return

    candidate_request = CandidateIDDTO(telegram_id=telegram_id)
    candidate = await usecase_candidate.get_candidate(candidate_request)

    await usecase_candidate.delete(candidate.id)
    await usecase_user.delete(user.id)

    await cq.bot.set_chat_menu_button(
        chat_id=cq.message.chat.id,
        menu_button=MenuButtonDefault()
    )

    await cq.message.answer(
        "🗑️ Ваша кандидатура успешно удалена.\n"
        "Для повторного участия введите /start",
        reply_markup=ReplyKeyboardRemove(),
    )

    await dialog_manager.done()
