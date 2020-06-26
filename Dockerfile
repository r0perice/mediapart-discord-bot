FROM python:3

ENV MEDIAPART_USER ""
ENV MEDIAPART_PWD ""
ENV BOT_TOKEN ""
ENV CHANNEL_ID ""
ENV BOT_FETCH_TIME_HOURS 1

RUN pip3 install -Iv mediapart_bot_core==1.0.0-beta.1 \
    &&  pip3 install discord configparser tinydb feedparser requests beautifulsoup4

ADD mediapart_bot.py .

CMD ["python3","mediapart_bot.py"]