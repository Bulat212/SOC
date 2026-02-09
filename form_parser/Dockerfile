FROM python:3.13.2

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src ./src

ENV PYTHONPATH=/app/src/form_parser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]