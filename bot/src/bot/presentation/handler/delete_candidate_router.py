from aiogram import F, Router
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from bot.application.dto.candidate import CandidateIDDTO
from bot.application.usecase.candidate import CandidateUseCase
from bot.presentation.state.delete_candidate import DeleteCandidateState
from dishka.integrations.aiogram import FromDishka, inject

from bot.application.dto.user import UserIDDTO
from bot.application.usecase.user import UserUseCase
from bot.domain.exception.info import InfoNotFound
from bot.domain.exception.user import UserNotFound

delete_candidate_router = Router()


@delete_candidate_router.message(F.text.lower() == "❌ удалить кандидатуру")
@inject
async def delete_handler(
        message: Message,
        dialog_manager: DialogManager,
        usecase: FromDishka[UserUseCase],
) -> None:
    await dialog_manager.reset_stack()
    request = UserIDDTO(
        telegram_id=str(message.from_user.id),
    )
    try:
        user = await usecase.get(request)
    except UserNotFound:
        return
    try:
        await dialog_manager.start(
            state=DeleteCandidateState.confirm,
            mode=StartMode.NORMAL,
        )
    except InfoNotFound:
        return


# @delete_candidate_router.message(F.text.lower() == "удалить мою кандидатуру")
# @inject
# async def delete_candidate_handler(
#         message: Message,
#         dialog_manager: DialogManager,
#         usecase_user: FromDishka[UserUseCase],
#         usecase_candidate: FromDishka[CandidateUseCase],
# ) -> None:
#     await dialog_manager.reset_stack()
#     telegram_id=str(message.from_user.id)
#     request = UserIDDTO(
#         telegram_id=telegram_id,
#     )
#     try:
#         user = await usecase_user.get(request)
#     except UserNotFound:
#         await message.answer("❗ Вы не зарегистрированы как кандидат.")
#         return
#     candidate_request = CandidateIDDTO(telegram_id=telegram_id)
#     candidate = await usecase_candidate.get_candidate(candidate_request)
    
#     await usecase_candidate.delete(candidate.id)
#     await usecase_user.delete(user.id)

#     await message.answer("🗑️ Ваша кандидатура успешно удалена. Для повторного участия в отборе введите /start")
    
