from aiogram.types import Message


def get_username_or_full_name(message: Message) -> str:
    if message.from_user.username is not None:
        return f"@{message.from_user.username}"
    return message.from_user.full_name


def get_reply_username_or_full_name(message: Message) -> str:
    if message.reply_to_message.from_user.username is not None:
        return f"@{message.reply_to_message.from_user.username}"
    return message.reply_to_message.from_user.full_name
