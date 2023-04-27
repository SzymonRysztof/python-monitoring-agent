FROM python:alpine

ARG user=python-agent
ARG uid=3000

RUN apk --no-cache add git gcc python3-dev build-base linux-headers \
    vim bash && \
	mkdir /app && chown 3000:3000 /app && \
    adduser --uid ${uid} --disabled-password -s /bin/sh -h /app ${user}

WORKDIR /app

COPY app /app

RUN chown -R ${user}:${user} /app

USER ${user}

RUN python3 -m pip install --no-cache-dir --upgrade -r requirements.txt && chmod +x /app/main.py

ENTRYPOINT ["/app/main.py"]
