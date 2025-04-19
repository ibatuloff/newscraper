FROM python:3.11-slim

WORKDIR /app

# зависимости
COPY reqs.txt .
RUN pip install --no-cache-dir -r reqs.txt

# файлы проекта
COPY newscraper ./newscraper
COPY scrapy.cfg .
COPY run_all.py .

CMD ["python", "run_all.py"]