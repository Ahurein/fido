FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

ENV HOST 0.0.0.0

CMD ["fastapi","run","src/main.py","--port","8080","--host","0.0.0.0"]
