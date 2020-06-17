FROM python:3

MAINTAINER Mike Peters "mike@skylake.me"

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

COPY ./discord_fivem_status_bot.py /discord_fivem_status_bot.py
COPY ./config.json /config.json
WORKDIR /

CMD ["python", "discord_fivem_status_bot.py"]