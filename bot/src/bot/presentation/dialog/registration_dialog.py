from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    ListGroup,
    Group,
    Row,
    RequestContact,
)
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const, Case, Format

from bot.presentation.func.registration import (
    set_last_name,
    set_first_name,
    set_patronymic,
    set_military_station,
    set_university,
    set_direction_training,
    set_average_score,
    set_find_out,
    set_phone_number,
    set_subject,
    set_birthdate,
    set_graduation_data,
    set_military_station_address,
)
from bot.presentation.getter.candidate import get_candidate
from bot.presentation.getter.recruitment import (
    check_recruitments,
    get_recruitments,
)
from bot.presentation.on_click.registration import (
    agreement_click,
    start_click,
    recruitment_click,
    nationality_click,
    invalid_nationality_click,
    invalid_tertiary_education_click,
    tertiary_education_click,
    right_click,
    incorrect_click,
)
from bot.presentation.state.registration import RegistrationCandidateState


def check_is_recruitments(
        data: dict,
        widget: Whenable,
        manager: DialogManager,
) -> bool:
    is_recruitments = data.get("is_recruitments")
    return is_recruitments


dialog = Dialog(
    Window(
        Const(
            text="Для участия в отборе в научную роту необходимо согласие на обработку Ваших данных. ",
        ),
        Button(
            text=Const(
                text="Согласен",
            ),
            id="next_btn",
            on_click=agreement_click,
        ),
        state=RegistrationCandidateState.agreement,
    ),
    Window(
        Case(
            texts={
                True: Const(
                    text="Для того, чтобы принять участие в отборе в научную роту, "
                         "ответьте, пожалуйста, на 16 вопросов.",
                ),
                False: Const(
                    text="Совсем скоро Вы сможете принять участие "
                         "в регистрации в отбор в научную роту.",
                ),
            },
            selector="is_recruitments",
        ),
        Button(
            text=Const(
                text="Ответить",
            ),
            id="next_btn",
            on_click=start_click,
            when=check_is_recruitments,
        ),
        state=RegistrationCandidateState.start,
        getter=check_recruitments,
    ),
    Window(
        Const(
            text="📋 Вопрос 16 из 16\nНа какой призыв Вы хотите оставить заявку?",
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
        state=RegistrationCandidateState.recruitment,
        getter=get_recruitments,
    ),
    Window(
        Const(
            text="📋 Вопрос 1 из 16\n🇷🇺Являетесь ли Вы гражданином Российской Федерации?",
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
        state=RegistrationCandidateState.nationality,
    ),
    Window(
        Const(
            text="Извините, наличие гражданства Российской Федерации является "
                 "обязательным условием для отбора в научную роту.",
        ),
        state=RegistrationCandidateState.invalid_nationality,
    ),
    Window(
        Const(
            text="📋 Вопрос 2 из 16\n🎓Имеется ли у Вас оконченное высшее техническое образование?",
        ),
        Button(
                text=Const(
                    text="В процессе обучения",
                ),
                on_click=tertiary_education_click,
                id="study_btn",
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
        state=RegistrationCandidateState.tertiary_education,
    ),
    Window(
        Const(
            text="Извините, наличие Высшего технического образования является "
                 "обязательным условием для отбора в научную роту.",
        ),
        state=RegistrationCandidateState.invalid_tertiary_education,
    ),
    Window(
        Const(
            text="📋 Вопрос 3 из 16\nНапишите свою дату рождения в формате (дд.мм.гггг).",
        ),
        MessageInput(
            func=set_birthdate,
        ),
        state=RegistrationCandidateState.birthdate,
    ),
    Window(
        Const(
            text="Введена некорректная дата, попробуйте снова.",
        ),
        MessageInput(
            func=set_birthdate,
        ),
        state=RegistrationCandidateState.invalid_birthdate,
    ),
    Window(
        Const(
            text="📋 Вопрос 7 из 16\nУкажите Ваш город:",
        ),
        MessageInput(
            func=set_subject,
        ),
        state=RegistrationCandidateState.subject,
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
        state=RegistrationCandidateState.invalid_period_birthdate,
    ),
    Window(
        Const(
            text="📋 Вопрос 4 из 16\nНапишите Вашу Фамилию.",
        ),
        MessageInput(
            func=set_last_name,
        ),
        state=RegistrationCandidateState.last_name,
    ),
    Window(
        Const(
            text="📋 Вопрос 5 из 16\nНапишите Ваше имя.",
        ),
        MessageInput(
            func=set_first_name,
        ),
        state=RegistrationCandidateState.first_name,
    ),
    Window(
        Const(
            text="📋 Вопрос 6 из 16\nНапишите Ваше отчество.",
        ),
        MessageInput(
            func=set_patronymic,
        ),
        state=RegistrationCandidateState.patronymic,
    ),
    Window(
        Const(
            text="📋 Вопрос 8 из 16\nНапишите полное название своего военного комиссариата:",
        ),
        MessageInput(
            func=set_military_station,
        ),
        state=RegistrationCandidateState.military_station,
    ),
    Window(
        Const(
            text="📋 Вопрос 9 из 16\nНапишите почтовый адрес и индекс "
                 "своего военного комиссариата:",
        ),
        MessageInput(
            func=set_military_station_address,
        ),
        state=RegistrationCandidateState.military_station_address,
    ),
    Window(
        Const(
            text="📋 Вопрос 10 из 16\nНапишите название своего ВУЗа.",
        ),
        MessageInput(
            func=set_university,
        ),
        state=RegistrationCandidateState.university,
    ),
    Window(
        Const(
            text="📋 Вопрос 11 из 16\nНапишите дату окончания ВУЗа в формате (дд.мм.гггг).",
        ),
        MessageInput(
            func=set_graduation_data,
        ),
        state=RegistrationCandidateState.graduation_date,
    ),
    Window(
        Const(
            text="Введена некорректная дата, попробуйте снова.",
        ),
        MessageInput(
            func=set_graduation_data,
        ),
        state=RegistrationCandidateState.invalid_graduation_date,
    ),
    Window(
        Const(
            text="📋 Вопрос 12 из 16\nНапишите направление подготовки в ВУЗе.",
        ),
        MessageInput(
            func=set_direction_training,
        ),
        state=RegistrationCandidateState.direction_training,
    ),
    Window(
        Const(
            text="📋 Вопрос 13 из 16\nНапишите средний балл по диплому (х.х).",
        ),
        MessageInput(
            func=set_average_score,
        ),
        state=RegistrationCandidateState.average_score,
    ),
    Window(
        Const(
            text="Введен некорректный балл, попробуйте снова.",
        ),
        MessageInput(
            func=set_average_score,
        ),
        state=RegistrationCandidateState.invalid_average_score,
    ),
    Window(
        Const(
            text="Ваш средний балл не соответствует требованиям. "
                 "В научную роту рассматриваются кандидаты со средним "
                 "баллом не менее 4.0.",
        ),
        state=RegistrationCandidateState.low_average_score,
    ),
    Window(
        Const(
            text="📋 Вопрос 14 из 16\nОткуда Вы узнали о нас?",
        ),
        MessageInput(
            func=set_find_out,
        ),
        state=RegistrationCandidateState.find_out,
    ),
    Window(
        Const(
            text="📋 Вопрос 15 из 16\nДля связи с Вами, нам необходимо получить Ваш номер "
                 "телефона. Нажмите на кнопку в меню, чтобы отправить его в чат.",
        ),
        MessageInput(
            func=set_phone_number,
        ),
        RequestContact(
            text=Const(
                text="Отправить номер телефона",
            ),
        ),
        state=RegistrationCandidateState.phone_number,
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
        state=RegistrationCandidateState.invalid_phone_number,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
            one_time_keyboard=False,
            is_persistent=True,
        ),
    ),
    Window(
        Format(
            text="Проверьте свои данные:\n\n"
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
        state=RegistrationCandidateState.check_data,
        getter=get_candidate,
    ),
)
