# Dockerfile

FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar o utilitário openssl
RUN apt-get update && apt-get install -y openssl

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /usr/src/app

COPY . .
COPY ./opportunity/.env /code/opportunity/.env


COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
