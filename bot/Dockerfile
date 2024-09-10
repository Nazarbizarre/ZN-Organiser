FROM python:3.11

WORKDIR /app/bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "bot.py"]