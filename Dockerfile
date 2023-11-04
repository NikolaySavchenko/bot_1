FROM python:alpine

MAINTAINER Savchenko Nikolay

WORKDIR /app_bot1

ARG DVMN_TOKEN=1
ENV DVMN_TOKEN="${DVMN_TOKEN}"
ARG TG_BOT_TOKEN=1
ENV TG_BOT_TOKEN="${TG_BOT_TOKEN}"
ARG TG_CHAT_ID=1
ENV TG_CHAT_ID="${TG_CHAT_ID}"

RUN pip install -U pip && pip install -r requirements.txt

COPY telebot.py .
COPY requirements.txt .
COPY README.md .

CMD [ "python", "telebot.py" ]