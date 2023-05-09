FROM python:alpine as builder

ARG user=python-agent
ARG uid=3000

RUN apk --no-cache add git gcc python3-dev build-base linux-headers && \
	mkdir /app /compiled && chown 3000:3000 /app && chown 3000:3000 /compiled && \
    adduser --uid ${uid} --disabled-password -s /bin/sh -h /app ${user}

WORKDIR /app
COPY . /app
RUN chown -R ${user}:${user} /app
USER ${user}
RUN python3 -m pip install --no-cache-dir .


FROM python:alpine

ARG user=python-agent
ARG uid=3000
WORKDIR /app
COPY --from=builder /app/.local/ /app/.local/

RUN adduser --uid ${uid} --disabled-password -s /bin/sh -h /app ${user} && \
    chown 3000:3000 /app

USER ${user}
ENTRYPOINT ["/app/.local/bin/pma"]