from aiogram import F
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Row,
    Group,
    ListGroup,
    RequestContact,
)
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Format, Const

from bot.presentation.func.my_data import (
    set_first_name,
    set_patronymic,
    set_last_name,
    set_military_station,
    set_university,
    set_birthdate,
    set_average_score,
    set_direction_training,
    set_phone_number,
    set_find_out,
    set_subject,
    set_graduation_data,
    set_military_station_address,
)
from bot.presentation.getter.candidate import get_candidate
from bot.presentation.getter.recruitment import get_recruitments
from bot.presentation.on_click.my_data import (
    set_recruitment_click,
    my_data_click,
    recruitment_click,
    first_name_click,
    patronymic_click,
    last_name_click,
    birthdate_click,
    nationality_click,
    military_station_click,
    university_click,
    average_score_click,
    direction_training_click,
    phone_number_click,
    find_out_click,
    save_click,
    set_nationality_click,
    invalid_nationality_click,
    subject_click,
    guarding_data_click,
    set_edit_click,
    military_station_address_click,
)
from bot.presentation.state.my_data import MyDataState


def check_is_save(
        data: dict[str, str],
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    return data.get("is_save", False)


dialog = Dialog(
    Window(
        Format(
            text="Ваши данные:\n\n"
                 "<b>Фамилия:</b> <u>{last_name}</u>\n"
                 "<b>Имя:</b> <u>{first_name}</u>\n"
                 "<b>Отчество:</b> <u>{patronymic}</u>\n"
                 "📆 <b>Дата рождения:</b> <u>{birthdate}</u>\n"
                 "🏙 <b>Город:</b> <u>{subject}</u>\n"
                 "🇷🇺 <b>Гражданство:</b> <u>{nationality}</u>\n"
                 "🪖 <b>Название военного комиссариата:</b> <u>{military_station}</u>\n"
                 "📬 <b>Почтовый адрес военного комиссариата, индекс:</b> <u>{military_station_address}</u>\n"
                 "🏫 <b>ВУЗ:</b> <u>{university}</u>\n"
                 "📆 <b>Дата окончания обучения:</b> <u>{graduation_date}</u>\n"
                #  "👨‍🎓 Уровень образования\n"
                 "🔬 <b>Направление подготовки:</b> <u>{direction_training}</u>\n"
                 "🌟 <b>Средний балл:</b> <u>{average_score}</u>\n"
                 "🫡 <b>Призыв:</b> <u>{recruitment}</u>\n"
                 "☎️ <b>Номер телефона:</b> <u>{phone_number}</u>\n"
                 "🔗 <b>Источник:</b> <u>{find_out}</u>",
        ),
        Button(
            text=Const(
                text="✏️ Редактировать",
            ),
            id="edit_btn",
            on_click=set_edit_click,
            when=~F["is_edit"],
        ),
        Button(
            text=Const(
                text="Призыв",
            ),
            id="recruitment_btn",
            on_click=recruitment_click,
            when=F["is_edit"],
        ),
        Row(
            Button(
                text=Const(
                    text="Фамилия",
                ),
                id="last_name_btn",
                on_click=last_name_click,
            ),
            Button(
                text=Const(
                    text="Имя",
                ),
                id="first_name_btn",
                on_click=first_name_click,
            ),
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Отчество",
            ),
            id="patronymic_btn",
            on_click=patronymic_click,
            when=F["is_edit"],
        ),
        Row(
            Button(
                text=Const(
                    text="Город",
                ),
                id="subject_btn",
                on_click=subject_click,
            ),
            Button(
                text=Const(
                    text="День рождения",
                ),
                id="birthdate_btn",
                on_click=birthdate_click,
            ),
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Гражданство",
            ),
            id="nationality_btn",
            on_click=nationality_click,
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Полное название военного комиссариата",
            ),
            id="military_station_btn",
            on_click=military_station_click,
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Почтовый адрес военного комиссариата, индекс",
            ),
            id="military_station_address_btn",
            on_click=military_station_address_click,
            when=F["is_edit"],
        ),
        Row(
            Button(
                text=Const(
                    text="ВУЗ",
                ),
                id="university_btn",
                on_click=university_click,
            ),
            Button(
                text=Const(
                    text="Дата окончания обучения",
                ),
                id="graduation_date_btn",
                on_click=guarding_data_click,
            ),
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Средний балл",
            ),
            id="average_score_btn",
            on_click=average_score_click,
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Направление подготовки",
            ),
            id="direction_training_btn",
            on_click=direction_training_click,
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Номер телефона",
            ),
            id="phone_number_btn",
            on_click=phone_number_click,
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Источник",
            ),
            id="find_out_btn",
            on_click=find_out_click,
            when=F["is_edit"],
        ),
        Button(
            text=Const(
                text="Сохранить ✅",
            ),
            id="save_btn",
            on_click=save_click,
            when=check_is_save,
        ),
        state=MyDataState.start,
        getter=get_candidate,
    ),
    Window(
        Const(
            text="На какой призыв Вы хотите оставить заявку?",
        ),
        Group(
            ListGroup(
                Button(
                    text=Format(
                        text="{item[name]}",
                    ),
                    id="recruitment_btn",
                    on_click=set_recruitment_click,
                ),
                id="recruitments",
                item_id_getter=lambda item: item["idx"],
                items="recruitments",
            ),
            width=2,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.recruitment,
        getter=get_recruitments,
    ),
    Window(
        Const(
            text="Напишите Ваше имя",
        ),
        MessageInput(
            func=set_first_name,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.first_name,
    ),
    Window(
        Const(
            text="Напишите Ваше отчество.",
        ),
        MessageInput(
            func=set_patronymic,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.patronymic,
    ),
    Window(
        Const(
            text="Напишите Вашу Фамилию.",
        ),
        MessageInput(
            func=set_last_name,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.last_name,
    ),
    Window(
        Const(
            text="Укажите Ваш город:",
        ),
        MessageInput(
            func=set_subject,
        ),
        state=MyDataState.subject,
    ),
    Window(
        Const(
            text="Напишите свою дату рождения в формате (дд.мм.гггг).",
        ),
        MessageInput(
            func=set_birthdate,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.birthdate,
    ),
    Window(
        Const(
            text="Напишите дату окончания ВУЗа в формате (дд.мм.гггг).",
        ),
        MessageInput(
            func=set_graduation_data,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.graduation_date,
    ),
    Window(
        Const(
            text="Введена некорректная дата, попробуйте снова.",
        ),
        MessageInput(
            func=set_birthdate,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.invalid_birthdate,
    ),
    Window(
        Const(
            text="Введена некорректная дата, попробуйте снова",
        ),
        MessageInput(
            func=set_graduation_data,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.invalid_graduation_date,
    ),
    Window(
        Const(
            text="В Соответствии с положениями п.п.\"а\", пункта 1, "
                 "статьи 22 \"Граждане, подлежащие призыву на военную "
                 "службу\" Федерального закона от 28.03.1998 N 53-ФЗ "
                 "(ред. от 02.10.2024) \"О воинской обязанности и военной "
                 "службе\", призыву на военную службу подлежат граждане "
                 "мужского пола в возрасте от 18 до 30 лет, состоящие "
                 "на воинском учете или не состоящие, но обязанные состоять "
                 "на воинском учете и не пребывающие в запасе",
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.invalid_period_birthdate,
    ),

    Window(
        Const(
            text="🇷🇺Являетесь ли Вы гражданином Российской Федерации?",
        ),
        Row(
            Button(
                text=Const(
                    text="Да",
                ),
                id="yes_btn",
                on_click=set_nationality_click,
            ),
            Button(
                text=Const(
                    text="Нет",
                ),
                id="no_btn",
                on_click=invalid_nationality_click,
            ),
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.nationality,
    ),
    Window(
        Const(
            text="Извините, наличие гражданства Российской Федерации является "
                 "обязательным условием для отбора в научную роту.",
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.invalid_nationality,
    ),
    Window(
        Const(
            text="Напишите название своего военного комиссариата.",
        ),
        MessageInput(
            func=set_military_station,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.military_station,
    ),
    Window(
        Const(
            text="Напишите почтовый адрес и индекс "
                 "своего военного комиссариата:",
        ),
        MessageInput(
            func=set_military_station_address,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.military_station_address,
    ),
    Window(
        Const(
            text="Напишите название своего ВУЗа.",
        ),
        MessageInput(
            func=set_university,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.university,
    ),
    Window(
        Const(
            text="Напишите средний балл по диплому (х.х).",
        ),
        MessageInput(
            func=set_average_score,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.average_score,
    ),
    Window(
        Const(
            text="Введен некорректный балл, попробуйте снова.",
        ),
        MessageInput(
            func=set_average_score,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.invalid_average_score,
    ),
    Window(
        Const(
            text="Ваш средний балл не соответствует требованиям. "
                 "В научную роту рассматриваются кандидаты со средним "
                 "баллом не менее 4.0.",
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.low_average_score,
    ),
    Window(
        Const(
            text="Напишите направление подготовки в ВУЗе.",
        ),
        MessageInput(
            func=set_direction_training,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.direction_training,
    ),
    Window(
        Const(
            text="Для связи с Вами, нам необходимо получить Ваш номер "
                 "телефона. Нажмите на кнопку в меню или напишите его в чат.",
        ),
        MessageInput(
            func=set_phone_number,
        ),
        RequestContact(
            text=Const(
                text="Отправить номер телефона",
            ),
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.phone_number,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
            one_time_keyboard=True,
            is_persistent=True,
        ),
    ),
    Window(
        Const(
            text="Неверный номер телефона! Повторите попытку снова!",
        ),
        MessageInput(
            func=set_phone_number,
        ),
        RequestContact(
            text=Const(
                text="Отправить номер телефона",
            ),
        ),
        state=MyDataState.invalid_phone_number,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
            one_time_keyboard=False,
            is_persistent=True,
        ),
    ),
    Window(
        Const(
            text="Откуда узнали о нас?",
        ),
        MessageInput(
            func=set_find_out,
        ),
        Button(
            text=Const(
                text="Мои данные",
            ),
            id="my_date_btn",
            on_click=my_data_click,
        ),
        state=MyDataState.find_out,
    ),
    Window(
        Const(
            text="Ваши данные изменены",
        ),
        state=MyDataState.save,
    ),
)
