from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class _StartKeyboardButton:
    def __init__(
            self,
            resize_keyboard: bool | None = None,
            one_time_keyboard: bool | None = None,
            is_persistent: bool | None = None,
    ) -> None:
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.is_persistent = is_persistent

    def _build(self,
            keyboard: list[list[KeyboardButton]],
    ) -> ReplyKeyboardMarkup:
        reply_keyboard_markup = ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=self.resize_keyboard,
            one_time_keyboard=self.one_time_keyboard,
            is_persistent=self.is_persistent,
        )
        return reply_keyboard_markup


class StartCandidateKeyboardButton(_StartKeyboardButton):
    def __call__(self) -> ReplyKeyboardMarkup:
        keyboard = [
            [
                KeyboardButton(
                    text="ℹ️ Инфо",
                ),
            ],
            [
                KeyboardButton(
                    text="👤 Мои данные",
                ),
                KeyboardButton(
                    text="📁 Мои документы",
                ),
            ],
            [
                KeyboardButton(
                    text="❓ Задать вопрос",
                ),
            ],
            [
                KeyboardButton(
                    text="🔍 Статус заявки",
                ),
                KeyboardButton(
                    text="❌ Удалить кандидатуру",
                ),
            ],
        ]
        return self._build(keyboard)


class StartDirectorKeyboardButton(_StartKeyboardButton):
    def __call__(self) -> ReplyKeyboardMarkup:
        keyboard = [
            [
                KeyboardButton(
                    text="Образцы документов кандидата",
                ),
                KeyboardButton(
                    text="Промо",
                ),
            ],
            [
                KeyboardButton(
                    text="Руководящие документы",
                ),
                KeyboardButton(
                    text="FAQ",
                ),
            ],
            [
                KeyboardButton(
                    text="Статистика по субъектам",
                ),
                KeyboardButton(
                    text="Статистика по представителям",
                ),
            ],
            [
                KeyboardButton(
                    text="Добавить представителя",
                ),
                KeyboardButton(
                    text="Список кандидатов",
                ),
            ],
            [
                KeyboardButton(
                    text="Входящие вопросы",
                ),
            ],
        ]
        return self._build(keyboard)


class StartDelegateKeyboardButton(_StartKeyboardButton):
    def __call__(self) -> ReplyKeyboardMarkup:
        keyboard = [
            [
                KeyboardButton(
                    text="ℹ️ Инфо",
                ),
            ],
            [
                KeyboardButton(
                    text="👤 Мои данные",
                ),
            ],
            [
                KeyboardButton(
                    text="Заполнить отчет",
                ),
                KeyboardButton(
                    text="Добавить кандидата",
                ),
            ],
            [
                KeyboardButton(
                    text="Результаты работы",
                ),
            ],
        ]
        return self._build(keyboard)


class CheckSubscriptionKeyboardButton(_StartKeyboardButton):
    def __call__(self) -> ReplyKeyboardMarkup:
        keyboard = [
            [
                KeyboardButton(
                    text="✅ Проверить подписку",
                ),
            ],
        ]
        return self._build(keyboard)
    

class DeleteCandidateDataKeyboardButton(_StartKeyboardButton):
    def __call__(self) -> ReplyKeyboardMarkup:
        keyboard = [
            [
                KeyboardButton(
                    text="Удалить мою кандидатуру",
                ),
            ],
        ]
        return self._build(keyboard)
