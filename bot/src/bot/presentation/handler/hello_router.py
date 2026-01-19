from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from bot.presentation.state.delegate import RegistrationDelegateState
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.domain.exception.user import UserNotFound
from bot.presentation.button.start_button import (
    StartCandidateKeyboardButton,
    StartDelegateKeyboardButton,
    StartDirectorKeyboardButton,
    CheckSubscriptionKeyboardButton,
)
from bot.presentation.state.registration import RegistrationCandidateState
from aiogram.exceptions import TelegramBadRequest
from bot.config import load_config

hello_router = Router()

HELLO_MESSAGE = {
    "candidate": "Здравствуйте, {username}!\n"
                 "Я - ГрОк. Виртуальный ассистент <b>Гр</b>уппы "
                 "по <b>О</b>тбору <b>К</b>андидатов в <b>Н</b>аучную <b>Р</b>оту.\n"
                 "Выберете интересующий Вас раздел 👇",
    "delegate": "Здравствуйте, {username}!\n"
                "Я - ГрОк. Я помогаю представителям <b>Гр</b>уппы "
                "по <b>О</b>тбору <b>К</b>андидатов в <b>Н</b>аучную <b>Р</b>оту.\n"
                "Выберете интересующий Вас раздел 👇",
    "director": "Здравствуйте, {username}!\n"
                "Я - ГрОк. Я помогаю руководителям <b>Гр</b>уппы "
                "по <b>О</b>тбору <b>К</b>андидатов в <b>Н</b>аучную <b>Р</b>оту.\n"
                "Выберете интересующий Вас раздел 👇",
    "not_role": "Здравствуйте, {username}!\n"
                "Я - ГрОк. Виртуальный ассистент <b>Гр</b>уппы "
                "по <b>О</b>тбору <b>К</b>андидатов в <b>Н</b>аучную <b>Р</b>оту.\n",
}


async def start_logic(
        message: Message,
        dialog_manager: DialogManager,
        usecase: UserUseCase,
) -> None:
    await dialog_manager.reset_stack(remove_keyboard=True)
    # config = load_config()
    # keyboard = CheckSubscriptionKeyboardButton( 
    #     resize_keyboard=True,
    #     one_time_keyboard=True,
    #     is_persistent=True,       
    # )
    # try:
    #     member = await message.bot.get_chat_member(config.channel_id, message.from_user.id)
    #     if member.status not in ("member", "administrator", "creator"):
    #         await message.answer(
    #             "❌ Для использования бота необходимо подписаться на канал:\n👉 @nrg_vas",
    #             reply_markup=keyboard(),
    #         )
    #         return
    # except TelegramBadRequest:
    #     await message.answer(
    #         f"⚠️ Не удалось проверить подписку. Попробуйте позже.",
    #         reply_markup=keyboard(),
    #     )
    #     return
    
    request = UserIDDTO(
        telegram_id=str(message.from_user.id),
    )
    try:
        user = await usecase.get(request=request)
        if user.is_active or user.role == "director":
            match user.role:
                case "candidate":
                    text = HELLO_MESSAGE[user.role].format(
                        username=message.from_user.full_name,
                    )
                    keyboard = StartCandidateKeyboardButton(
                        resize_keyboard=True,
                        one_time_keyboard=False,
                        is_persistent=True,
                    )
                case "delegate":
                    text = HELLO_MESSAGE[user.role].format(
                        username=message.from_user.full_name,
                    )
                    keyboard = StartDelegateKeyboardButton(
                        resize_keyboard=True,
                        one_time_keyboard=False,
                        is_persistent=True,
                    )
                case "director":
                    text = HELLO_MESSAGE[user.role].format(
                        username=message.from_user.full_name,
                    )
                    keyboard = StartDirectorKeyboardButton(
                        resize_keyboard=True,
                        one_time_keyboard=False,
                        is_persistent=True,
                    )
            await message.answer(
                text=text,  # noqa
                reply_markup=keyboard(),  # noqa
            )
            return
        elif user.is_active == False and user.role == "delegate":
            await dialog_manager.start(
                state=RegistrationDelegateState.start,
                mode=StartMode.NORMAL,
                data={
                    "username": message.from_user.username,
                    "user_id": message.from_user.id,
                    "first_name": message.from_user.first_name,
                    "last_name": message.from_user.last_name,
                    "role": user.role,
                },
                show_mode=ShowMode.DELETE_AND_SEND,
            )
            return
        # TODO: Добавить регистрацию для представителей
        return
    except UserNotFound:
        role = "candidate"
    await message.answer(
        text=HELLO_MESSAGE["not_role"].format(
            username=message.from_user.full_name,
        ),
    )
    await dialog_manager.start(
        state=RegistrationCandidateState.start,
        mode=StartMode.NORMAL,
        data={
            "username": message.from_user.username,
            "user_id": message.from_user.id,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "role": role,
        },
        show_mode=ShowMode.DELETE_AND_SEND,
    )


@hello_router.message(CommandStart())
@inject
async def start_command(
    message: Message,
    dialog_manager: DialogManager,
    usecase: FromDishka[UserUseCase],
):
    await start_logic(message, dialog_manager, usecase)


@hello_router.message(F.text == "✅ Проверить подписку")
@inject
async def check_subscription_again(
    message: Message,
    dialog_manager: DialogManager,
    usecase: FromDishka[UserUseCase]
):
    await start_logic(message, dialog_manager, usecase)