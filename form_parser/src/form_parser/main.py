from fastapi import FastAPI, Request
from faststream.rabbit import RabbitBroker
from contextlib import asynccontextmanager
import re
import datetime
import asyncio
import json

from producer.form_producer import FormProducer
from dto.form import FormDataDTO
from config.config import RabbitSOCSettings


settings = RabbitSOCSettings()
broker_soc = RabbitBroker(settings.url)
soc_producer = FormProducer(broker_soc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker_soc.start()

    yield

    await broker_soc.close()

app = FastAPI(lifespan=lifespan)

def clean_text(text: str) -> str:
    result = text.replace("Узнал о научной роте:", "").strip()
    return result

def get_health_category(data5, data4, data3, data2, data1):
    if data5:
        return data5
    elif data4:
        return data4
    elif data3:
        return data3
    elif data2:
        return data2
    elif data1:
        return data1
    else:
        return None



@app.post("/webhook/forms")
async def webhook(request: Request):
    
    payload = await request.json()

    raw_data = payload.get("params", {}).get("data")
    form_json = json.loads(raw_data)

    form_json["Дата рождения"] = datetime.datetime.strptime(
            form_json.get("Дата рождения"),
            "%Y-%m-%d",
        ).isoformat() if form_json.get("Дата рождения") else None
    
    form_json["Дата окончания обучения в ВУЗе"] = datetime.datetime.strptime(
        form_json.get("Дата окончания обучения в ВУЗе"),
        "%Y-%m-%d",
    ).isoformat() if form_json.get("Дата окончания обучения в ВУЗе") else None

    form_json["Дата выдачи диплома"] = datetime.datetime.strptime(
        form_json.get("Дата выдачи диплома"),
        "%Y-%m-%d",
    ).isoformat() if form_json.get("Дата выдачи диплома") else None

    find_out = clean_text(form_json["Дополнительная информация"])

    health_category = get_health_category(form_json.get("Не годен к военной службе:"), 
                                          form_json.get("Временно не годен к военной службе:"),
                                          form_json.get("Ограниченно годен к военной службе:"),
                                          form_json.get("Годен к военной службе с незначительными ограничениями:"),
                                          form_json.get("Годен к военной службе:"),
                                          )

    form_data = FormDataDTO(
        candidate_id=form_json.get("candidate_id"),
        telegram_id=form_json.get("telegram_id"),
        first_name=form_json.get("Имя"),
        last_name=form_json.get("Фамилия"),
        patronymic=form_json.get("Отчество"),
        birthplace=form_json.get("Место рождения"),
        birthdate=form_json.get("Дата рождения"),
        graduation_date=form_json.get("Дата окончания обучения в ВУЗе"),
        nationality=form_json.get("Гражданство"),
        tg_username=form_json.get("tg_username"),
        mail=form_json.get("Электронная почта"),
        registration_address=form_json.get("Адрес регистрации"),
        actual_address=form_json.get("Адрес фактического проживания"),
        family_status=form_json.get("Семейное положение"),
        military_station=form_json.get("Наименование отдела военного комиссариата, в котором гражданин состоит на учете"),
        health_category=health_category,
        university=form_json.get("Полное наименование учебного заведения"),
        diploma=form_json.get("Наличие и наименование документа государственного образца о высшем образовании"),
        date_issue_diploma=form_json.get("Дата выдачи диплома"),
        direction_training=form_json.get("Наименование специальности высшего образования (направление подготовки)"),
        average_score=form_json.get("Средний балл согласно диплому с учетом оценок, за практики и курсовые проекты"),
        diploma_topic=form_json.get("Тема выпускной квалификационной работы"),
        international_articles=form_json.get("Научные статьи, опубликованные в международных изданиях"),
        patents=form_json.get("Патенты на изобретения и полезные модели"),
        vac_articles=form_json.get("Научных статьи, опубликованные в научных изданиях, рекомендуемых ВАК"),
        rationalization=form_json.get("Свидетельства на рационализаторские предложения"),
        rinc_articles=form_json.get("Научные статьи, опубликованные в изданиях РИНЦ"),
        registration_certificates=form_json.get("Свидетельства о регистрации баз данных и программ для ЭВМ"),
        scientific_work_experience=form_json.get("Опыт научной работы (с указанием направления и тематики работы)"),
        international_olympiads=form_json.get("Призовые места на международных олимпиадах"),
        president_scholarship=form_json.get("Государственные стипендий Президента РФ"),
        russian_olympiads=form_json.get("Призовые места на олимпиадах всероссийского уровня"),
        government_scholarship=form_json.get("Государственные стипендии Правительства РФ"),
        grant=form_json.get("Гранты по научным работам, имеющим прикладное значение для Министерства Обороны РФ, подтвержденные органами военного управления"),
        regional_olympiads=form_json.get("Призовые места на олимпиадах областного уровня"),
        city_olympiads=form_json.get("Призовые места на олимпиадах городского уровня"),
        postgraduate_diploma=form_json.get("Наличие диплома об успешном усвоении программы подготовки кадров высшей квалификации (аспирантуры)"),
        unused_academic_degree=form_json.get("Наличие ученой степени по специальности, не соответствующей профилю научных исследований научной работы"),
        useful_academic_degree=form_json.get("Наличие ученой степени по специальности, соответствующей профилю научных исследований научной работы"),
        commercial_experience=form_json.get("Работа в коммерческих предприятиях"),
        OPK_experience=form_json.get("Работа на предприятиях ОПК"),
        exp_research_assistant=form_json.get("Работа в научных организациях (подразделениях) на должностях научных сотрудников"),
        areas_research=form_json.get("Планируемые направления исследований (научной деятельности)"),
        programming_languages=form_json.get("Знание языков программирования"),
        programs=form_json.get("Знание программных продуктов"),
        secret=form_json.get("Отношение гражданина к оформлению допуска к сведениям. Содержащим государственную тайну (согласен или не согласен, форма допуска 1, 2 или 3)"),
        height=form_json.get("Рост"),
        weight=form_json.get("Вес"),
        sporting_achievements=form_json.get("Наличие спортивных достижений по военно-прикладным видам спорта, в том числе выполнение нормативов ГТО"),
        other_sporting_achievements=form_json.get("Наличие спортивных достижений по иным видам спорта"),
        short_run=form_json.get("Время за 100 м"),
        long_run=form_json.get("Время за 3 км (1 км)"),
        pull_ups=form_json.get("Подтягивания на перекладине"),
        chronic_diseases=form_json.get("Хронические, приобретенные заболевания; перенесенные операции"),
        tattoos=form_json.get("Отношение к пирсингу и татуировкам (наличие на теле)"),
        find_out=find_out,
    )
    print(form_data)
    
    await soc_producer.update_form_data(form_data)


    return {"status": "queued"}
