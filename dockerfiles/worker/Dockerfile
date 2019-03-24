FROM python:3.6-alpine

WORKDIR app

RUN apk add gcc musl-dev libffi-dev make openssl-dev

COPY requirements requirements
RUN pip3 install -r requirements/base.txt && \
    pip3 install -r requirements/misc-deps.txt


COPY . .

ENTRYPOINT celery -A entry_worker worker -l debug -Q tasks -n tasks
