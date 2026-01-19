from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, ListGroup, Group, Row
from aiogram_dialog.widgets.text import Const, Format


from bot.presentation.getter.candidate import get_candidate

from bot.presentation.func.add_candidate import (
    set_birthdate,
    set_last_name,
    set_first_name,
    set_military_station_address, set_patronymic, set_military_station, set_university,set_subject,
    set_graduation_data, set_direction_training, set_average_score, set_find_out, set_phone_number,
)
from bot.presentation.getter.recruitment import (
    get_recruitments,
)
from bot.presentation.on_click.add_candidate import (
    start_click,
    recruitment_click,
    nationality_click,
    invalid_nationality_click,
    invalid_tertiary_education_click,
    tertiary_education_click,
    right_click,
    incorrect_click,

)
from bot.presentation.state.add_candidate import AddCandidateState


# def check_is_recruitments(
#         data: dict,
#         widget: Whenable,
#         manager: DialogManager,
# ) -> bool:
#     is_recruitments = data.get("is_recruitments")
#     return is_recruitments


dialog = Dialog(
    Window(
        Const(
            text="Для того, чтобы добавить кандидата "
                    "ответьте на несколько вопросов.",
        ),
        Button(
            text=Const(
                text="Ответить",
            ),
            id="next_btn",
            on_click=start_click
        ),
        state=AddCandidateState.start
    ),
    Window(
        Const(
            text="На какой призыв кандидат хочет оставить заявку?",
        ),
        Group(
            ListGroup(
                Button(
                    text=Format(
                        text="{item[name]}",
                    ),
                    id="recruitment_btn",
                    on_click=recruitment_click,
                ),
                id="recruitments",
                item_id_getter=lambda item: item["idx"],
                items="recruitments",
            ),
            width=2,
        ),
        state=AddCandidateState.recruitment,
        getter=get_recruitments,
    ),
    Window(
        Const(
            text="🇷🇺Является ли кандидат гражданином Российской Федерации?",
        ),
        Row(
            Button(
                text=Const(
                    text="Да",
                ),
                id="yes_btn",
                on_click=nationality_click,
            ),
            Button(
                text=Const(
                    text="Нет",
                ),
                id="no_btn",
                on_click=invalid_nationality_click,
            ),
        ),
        state=AddCandidateState.nationality,
    ),
    Window(
        Const(
            text="Извините, наличие гражданства Российской Федерации является "
                 "обязательным условием для отбора в научную роту.",
        ),
        state=AddCandidateState.invalid_nationality,
    ),
    Window(
        Const(
            text="🎓Имеется ли у кандидата оконченное высшее техническое образование?",
        ),
        Row(
            Button(
                text=Const(
                    text="Да",
                ),
                on_click=tertiary_education_click,
                id="yes_btn",
            ),
            Button(
                text=Const(
                    text="Нет",
                ),
                id="no_btn",
                on_click=invalid_tertiary_education_click,
            ),
        ),
        state=AddCandidateState.tertiary_education,
    ),
    Window(
        Const(
            text="Извините, наличие Высшего технического образования является "
                 "обязательным условием для отбора в научную роту.",
        ),
        state=AddCandidateState.invalid_tertiary_education,
    ),
    Window(
        Const(
            text="Напишите дату рождения кандидата в формате (дд.мм.гггг).",
        ),
        MessageInput(
            func=set_birthdate,
        ),
        state=AddCandidateState.birthdate,
    ),
    Window(
        Const(
            text="Введена некорректная дата, попробуйте снова.",
        ),
        MessageInput(
            func=set_birthdate,
        ),
        state=AddCandidateState.invalid_birthdate,
    ),
    Window(
        Const(
            text="Напишите Ваш город:",
        ),
        MessageInput(
            func=set_subject,
        ),
        state=AddCandidateState.subject,
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
        state=AddCandidateState.invalid_period_birthdate,
    ),
    Window(
        Const(
            text="Напишите Фамилию кандидата.",
        ),
        MessageInput(
            func=set_last_name,
        ),
        state=AddCandidateState.last_name,
    ),
    Window(
        Const(
            text="Напишите имя кандидата.",
        ),
        MessageInput(
            func=set_first_name,
        ),
        state=AddCandidateState.first_name,
    ),
    Window(
        Const(
            text="Напишите отчество кандидата.",
        ),
        MessageInput(
            func=set_patronymic,
        ),
        state=AddCandidateState.patronymic,
    ),
    Window(
        Const(
            text="Напишите полное название военного комиссариата кандидата.",
        ),
        MessageInput(
            func=set_military_station,
        ),
        state=AddCandidateState.military_station,
    ),
    Window(
        Const(
            text="Напишите почтовый адрес и индекс "
                 "военного комиссариата кандидата:",
        ),
        MessageInput(
            func=set_military_station_address,
        ),
        state=AddCandidateState.military_station_address,
    ),
    Window(
        Const(
            text="Напишите название ВУЗа кандидата.",
        ),
        MessageInput(
            func=set_university,
        ),
        state=AddCandidateState.university,
    ),
    Window(
        Const(
            text="Напишите дату окончания ВУЗа кандидатом в формате (дд.мм.гггг).",
        ),
        MessageInput(
            func=set_graduation_data,
        ),
        state=AddCandidateState.graduation_date,
    ),
    Window(
        Const(
            text="Введена некорректная дата, попробуйте снова.",
        ),
        MessageInput(
            func=set_graduation_data,
        ),
        state=AddCandidateState.invalid_graduation_date,
    ),
    Window(
        Const(
            text="Напишите направление подготовки кандидата в ВУЗе.",
        ),
        MessageInput(
            func=set_direction_training,
        ),
        state=AddCandidateState.direction_training,
    ),
    Window(
        Const(
            text="Напишите средний балл кандидата по диплому (х.х).",
        ),
        MessageInput(
            func=set_average_score,
        ),
        state=AddCandidateState.average_score,
    ),
    Window(
        Const(
            text="Введен некорректный балл, попробуйте снова.",
        ),
        MessageInput(
            func=set_average_score,
        ),
        state=AddCandidateState.invalid_average_score,
    ),
    Window(
        Const(
            text="Средний балл кандидата не соответствует требованиям. "
                 "В научную роту рассматриваются кандидаты со средним "
                 "баллом не менее 4.0.",
        ),
        state=AddCandidateState.low_average_score,
    ),
    Window(
        Const(
            text="Откуда кандидат узнал о нас?",
        ),
        MessageInput(
            func=set_find_out,
        ),
        state=AddCandidateState.find_out,
    ),
    Window(
        Const(
            text="Для связи с кандидатом, нам необходимо получить номер его телефона "
                "Напишите его в чат.",
        ),
        MessageInput(
            func=set_phone_number,
        ),
        state=AddCandidateState.phone_number,
    ),
    Window(
        Const(
            text="Неверный номер телефона! Повторите попытку снова!",
        ),
        MessageInput(
            func=set_phone_number,
        ),
        state=AddCandidateState.invalid_phone_number,
    ),
    Window(
        Format(
            text="Проверьте данные кандидата:\n\n"
                 "<b>Фамилия:</b> <u>{last_name}</u>\n"
                 "<b>Имя:</b> <u>{first_name}</u>\n"
                 "<b>Отчество:</b> <u>{patronymic}</u>\n"
                 "🏙 <b>Город:</b> <u>{subject}</u>\n"
                 "📆 <b>Дата рождения:</b> <u>{birthdate}</u>\n"
                 "🇷🇺 <b>Гражданство:</b> <u>{nationality}</u>\n"
                 "🪖 <b>Название военного комиссариата:</b> <u>{military_station}</u>\n"
                 "🏫 <b>ВУЗ:</b> <u>{university}</u>\n"
                 "📆 <b>Дата окончания обучения:</b> <u>{graduation_date}</u>\n"
                 "👨‍🎓 Уровень образования\n"
                 "🔬 <b>Направление подготовки:</b> <u>{direction_training}</u>\n"
                 "🌟 <b>Средний балл:</b> <u>{average_score}</u>\n"
                 "🫡 <b>Призыв:</b> <u>{recruitment}</u>\n"
                 "☎️ <b>Номер телефона:</b> <u>{phone_number}</u>\n"
                 "🔗 <b>Источник:</b> <u>{find_out}</u>",
        ),
        Row(
            Button(
                text=Const(
                    text="Верно",
                ),
                id="right_btn",
                on_click=right_click,
            ),
            Button(
                text=Const(
                    text="Неверно",
                ),
                id="incorrect_btn",
                on_click=incorrect_click,
            ),
        ),
        state=AddCandidateState.check_data,
        getter=get_candidate,
    ),
)