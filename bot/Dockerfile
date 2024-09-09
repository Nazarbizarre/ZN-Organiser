FROM python:3.9-slim

WORKDIR /app/bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python" "bot.py"]