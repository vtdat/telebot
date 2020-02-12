FROM python:3

RUN pip install python-telegram-bot requests

ADD . /

CMD [ "python", "./bot.py" ]