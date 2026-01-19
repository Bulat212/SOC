from aiogram.types import Message, File
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from bot.presentation.state.promo import PromoState


async def set_promo_name(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    text = message.text
    manager.start_data["name"] = text
    await manager.switch_to(
        state=PromoState.adding_file,
    )


MEDIA = ("document", "photo", "video")


async def set_promo_document(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
) -> None:
    file = None
    for media in MEDIA:
        if not getattr(message, media):
            continue
        file = getattr(message, media)
    if file is None:
        await manager.switch_to(
            state=PromoState.adding_file,
        )
        return
    file_info: File = await message.bot.get_file(file_id=file.file_id)
    file_path = file_info.file_path
    manager.start_data["file_path"] = file_path
    await manager.switch_to(
        state=PromoState.save_file,
    )
