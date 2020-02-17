FROM python:3.8-alpine
WORKDIR /app

RUN apk --no-cache  add gcc musl-dev

RUN pip3 install pipenv==2018.11.26 --no-cache-dir

COPY Pipfile* /app/

RUN pipenv install --system --deploy

COPY . /app
