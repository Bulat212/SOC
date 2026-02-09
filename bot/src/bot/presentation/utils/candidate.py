import datetime
from bot.constants import FORMAT_BIRTHDATE
from urllib.parse import urlencode


def format_new_candidate_message(data: dict) -> str:
    username = data.get("username")
    username_text = f"@{username}" if username else "без username"

    birthdate = datetime.datetime.strptime(
        data.get("birthdate"),
        FORMAT_BIRTHDATE,
    ).strftime("%d.%m.%Y")

    graduation_date = datetime.datetime.strptime(
        data.get("graduation_date"),
        FORMAT_BIRTHDATE,
    ).strftime("%d.%m.%Y")

    return (
        "✅ <b>Зарегистрирована новая заявка от пользователя</b> "
        f"{username_text}\n\n"
        f"Фамилия: <u>{data.get('last_name')}</u>\n"
        f"Имя: <u>{data.get('first_name')}</u>\n"
        f"Отчество: <u>{data.get('patronymic')}</u>\n"
        f"📆 Дата рождения: <u>{birthdate}</u>\n"
        f"🏙 Город: <u>{data.get('subject')}</u>\n"
        f"🇷🇺 Гражданство: <u>{data.get('nationality')}</u>\n"
        f"🪖 Название военного комиссариата: <u>{data.get('military_station')}</u>\n"
        f"📬 Почтовый адрес военного комиссариата, индекс: <u>{data.get('military_station_address')}</u>\n"
        f"🏫 ВУЗ: <u>{data.get('university')}</u>\n"
        f"📆 Дата окончания обучения: <u>{graduation_date}</u>\n"
        f"🔬 Направление подготовки: <u>{data.get('direction_training')}</u>\n"
        f"🌟 Средний балл: <u>{data.get('average_score')}</u>\n"
        f"🫡 Призыв: <u>{data.get('recruitment').get('name')}</u>\n"
        f"☎️ Номер телефона: <u>{data.get('phone_number')}</u>\n"
        f"🔗 Источник: <u>{data.get('find_out')}</u>"
    )


def create_yandex_form_url(data, username) ->str: 

    params = {
        "first_name": data.first_name,
        "last_name": data.last_name,
        "patronymic": data.patronymic,
        "telegram_id": data.telegram_id,
        "candidate_id": data.id,
        "tg_username": username,
        "birthdate": data.birthdate,
        "nationality": "nationality_rf",
        "military_station": data.military_station,
        "university": data.university,
        "direction_training": data.direction_training,
        "average_score": data.average_score,
        "graduation_date": data.graduation_date,
        "find_out": f"Узнал о научной роте: {data.find_out}",
    }

    url = "https://forms.yandex.ru/u/694be999d046887fae3691b6?" + urlencode(
        params,
        doseq=True,
        encoding="utf-8",
    )
    return url
