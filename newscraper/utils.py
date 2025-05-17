from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from newscraper.spiders.kaspersky_spider import KasperskySpider
import asyncio
from fastapi import FastAPI, HTTPException
import uvicorn
from threading import Lock
import time

def run_all_spiders(process):
    process.crawl(KasperskySpider)
    process.start()