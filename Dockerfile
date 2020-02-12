FROM python:3-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install python-telegram-bot requests \
    && apt-get purge -y --auto-remove gcc

ADD . /

CMD [ "python", "./bot.py" ]