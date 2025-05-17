FROM python:3.11-slim

WORKDIR /app

# зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# сертификат yandex cloud

COPY certificate certificate

# RUN apt-get update && apt-get install -y wget && \ 
#     mkdir -p ./.postgresql && \ 
#     wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \ 
#     --output-document ./.postgresql/root.crt && \ 
#     chmod 0655 ./.postgresql/root.crt


# файлы проекта
COPY newscraper newscraper 
COPY scrapy.cfg .
COPY run_all.py .

CMD ["python", "run_all.py"]