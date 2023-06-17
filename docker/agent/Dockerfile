FROM python:alpine as builder

ARG user=python-agent
ARG uid=3000

RUN apk --no-cache add git gcc python3-dev build-base linux-headers docker && \
	mkdir /app /compiled && chown ${uid}:${uid} /app && chown ${uid}:${uid} /compiled && \
    adduser --uid ${uid} --disabled-password -s /bin/sh -h /app ${user}

WORKDIR /app
COPY . /app
RUN chown -R ${user}:${user} /app
USER ${user}
RUN python3 -m pip install --no-cache-dir .


FROM python:alpine

ARG user=python-agent
ARG uid=3000
ENV user=${user}
WORKDIR /app
COPY --from=builder /app/.local/ /app/.local/
COPY --from=builder /usr/bin/docker /usr/bin/docker
COPY entrypoint.sh /entrypoint.sh

RUN adduser --uid ${uid} --disabled-password -s /bin/sh -h /app ${user} && \
    chown ${uid}:${uid} /app

CMD ["sh", "/entrypoint.sh"]