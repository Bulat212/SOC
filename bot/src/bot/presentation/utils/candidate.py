import datetime
from bot.constants import FORMAT_BIRTHDATE
from urllib.parse import urlencode
from typing import List, Dict, Any, Optional
import re

from bot.config import load_config


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
    config = load_config()
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
    url = config.yandex_form_url + urlencode(
        params,
        doseq=True,
        encoding="utf-8",
    )
    return url




def filter_recruitments_by_date(
    recruitments: List[Dict[str, Any]],
    check_date: Optional[datetime.datetime] = None
) -> List[Dict[str, Any]]:
    if check_date is None:
        check_date = datetime.datetime.now()
    
    current_year = check_date.year
    current_month = check_date.month
    current_day = check_date.day
    
    july_pattern = re.compile(r'^Июль\s+(\d{4})$')
    december_pattern = re.compile(r'^Декабрь\s+(\d{4})$')
    
    filtered = []
    for recruitment in recruitments:
        name = recruitment.get("name", "")
       
        july_match = july_pattern.match(name)
        if july_match:
            recruitment_year = int(july_match.group(1))
            # Скрыть, если текущая дата после 25 марта
            if current_month > 3 or (current_month == 3 and current_day > 25) or current_year > recruitment_year:
                continue
        
        # Проверка для "Декабрь YYYY"
        december_match = december_pattern.match(name)
        if december_match:
            recruitment_year = int(december_match.group(1))
            # Скрыть, если текущая дата после 25 сентября
            if current_month > 9 or (current_month == 9 and current_day > 25) or current_year > recruitment_year:
                continue
        
        filtered.append(recruitment)
    
    return filtered