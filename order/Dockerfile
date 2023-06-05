# Dockerfile

FROM python:3.10.0-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ./order

RUN chmod +x /app/order/entrypoint.sh
ENTRYPOINT ["/app/order/entrypoint.sh"]

EXPOSE 8000