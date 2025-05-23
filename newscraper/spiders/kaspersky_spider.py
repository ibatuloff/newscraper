from newscraper.basic_spider import BasicSpider
from newscraper.items import ArticleItem
import os
import re
from datetime import datetime, timedelta, timezone
import dateparser
from scrapy import Request

class KasperskySpider(BasicSpider):
    name = 'kaspersky'
    allowed_domains = ['kaspersky.ru']
    site_url = 'https://www.kaspersky.ru'
    site_name = 'kaspersky.ru'
    start_urls = ['https://www.kaspersky.ru/about/press-releases']

    def parse(self, response):
        timeframe = int(os.getenv("TIMEFRAME", '7'))
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=timeframe)

        for card in response.css("div[data-at-selector='media-card']"):
            article_date = card.css("span[data-date]::text").get()
            article_date = dateparser.parse(article_date, languages=['ru']).replace(tzinfo=timezone.utc)
            if article_date >= cutoff_date: # статья "старше" чем  не будет собрана
                article_link = card.css("h3 a").attrib.get("href")
                title = card.css("h3 a::text").get()
                yield response.follow(article_link, callback=self.parse_article, meta={
                    "grid_url": response.url,
                    "title": title,
                    "date": article_date
                })


    def parse_article(self, response):
        item = ArticleItem()
        grid_url = response.meta['grid_url']
        item['title'] = response.meta['title']
        item['date'] = response.meta['date']
        item['url'] = response.url
        article_content = [text.strip() for text in response.css("div[class^='ArticleBody_content_']").xpath("string()").getall()]
        item['content'] = '\n'.join(article_content)

        yield item
