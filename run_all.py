from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from newscraper.spiders.kaspersky_spider import KasperskySpider
from newscraper.spiders.angarasecurity_spider import AngaraSecuritySpider
from newscraper.spiders.securityvision_spider import SecurityVesionSpider
from dotenv import load_dotenv

load_dotenv("/app/.env")
settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(KasperskySpider)
process.crawl(AngaraSecuritySpider)
process.crawl(SecurityVesionSpider)
process.start()


