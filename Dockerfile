FROM python:3

ENV MEDIAPART_USER ""
ENV MEDIAPART_PWD ""
ENV BOT_TOKEN ""
ENV CHANNEL_ID ""
ENV BOT_FETCH_TIME_HOURS 1

RUN pip3 install -Iv mediapart-parser==1.0.4 \
    && pip3 install -Iv discord.py==1.4.1 \
    && pip3 install -Iv configparser==5.0.0  \
    && pip3 install -Iv tinydb==4.1.1 \
    && pip3 install -Iv feedparser==5.2.1 \
    && pip3 install -Iv requests==2.24.0 \
    && pip3 install -Iv beautifulsoup4==4.9.1

ADD mediapart_bot.py .

CMD ["python3","mediapart_bot.py"]