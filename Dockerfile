FROM python:3.12-slim

WORKDIR /app

# зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y cron

# сертификат yandex cloud
RUN apt-get update && apt-get install -y wget && \ 
    mkdir -p ./certificate && \ 
    wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \ 
    --output-document ./certificate/RootCA.pem && \ 
    chmod 0655 ./certificate/RootCA.pem

# файлы проекта
COPY newscraper newscraper 
COPY scrapy.cfg .
COPY run_all.py .
COPY .env .env

COPY crontask /etc/cron.d/crontask
RUN chmod 0644 /etc/cron.d/crontask && crontab /etc/cron.d/crontask
RUN mkdir -p /var/log/cronlogs

CMD cron -f