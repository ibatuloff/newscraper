import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from newscraper.spiders.kaspersky_spider import KasperskySpider
from newscraper.pipelines import DatabasePipeline
from newscraper.items import Article


settings = get_project_settings()

    # Create a CrawlerProcess with the loaded settings
process = CrawlerProcess(settings)
process.crawl(KasperskySpider)
# item = Article(title='Test Article', summary='Test Summary', date='2025-04-19', url='https://example.com', content='Test content')

# Test the pipeline
# pipeline = DatabasePipeline("postgresql://admin:supersecretpassword@localhost:5432/newsdb")
# pipeline.process_item(item, kaspersky_spider.KasperskySpider())
process.start()
