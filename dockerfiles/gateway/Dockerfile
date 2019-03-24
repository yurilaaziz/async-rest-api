FROM python:3.6-alpine

WORKDIR app

RUN apk add gcc musl-dev libffi-dev make openssl-dev

COPY requirements requirements
RUN pip install -r requirements/base.txt && \
    pip install -r requirements/misc-deps.txt &&\
    pip install gunicorn


COPY . .

ENTRYPOINT gunicorn -b 0.0.0.0:8000 barberousse.api:app
