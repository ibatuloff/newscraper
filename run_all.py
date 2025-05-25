from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from newscraper.spiders.kaspersky_spider import KasperskySpider
from newscraper.spiders.angarasecurity_spider import AngaraSecuritySpider
from newscraper.spiders.securityvision_spider import SecurityVisionSpider
from newscraper.spiders.rtsolar_spider import RTSolarSpider
from newscraper.spiders.infotecs_spider import InfoTecSpider
from dotenv import load_dotenv

load_dotenv("/app/.env")
settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(KasperskySpider)
process.crawl(AngaraSecuritySpider)
process.crawl(SecurityVisionSpider)
process.crawl(RTSolarSpider)
process.crawl(InfoTecSpider)
process.start()


