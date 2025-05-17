from newscraper.basic_spider import BasicSpider
from newscraper.items import ArticleItem
import os
import re
from datetime import datetime, timedelta, timezone
import dateparser
from scrapy import Request


class AngaraSecuritySpider(BasicSpider):
    name = 'angarasecurity'
    allowed_domains = ['ptsecurity.com']
    site_url = 'https://www.angarasecurity.ru'
    site_name = 'angarasecurity.ru'
    start_urls = ['https://www.angarasecurity.ru/stati/']

    def parse(self, response):
        timeframe = int(os.getenv("TIMEFRAME", '7'))
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=timeframe)

        for card in response.css("div[class*='section-articles__content'] a[id^='bx']"):
            article_date = card.css("div[class*='section-event__date'] p::text").get()
            article_date = dateparser.parse(article_date, languages=['ru']).replace(tzinfo=timezone.utc)

            if article_date >= cutoff_date:  # статья "старше" чем  не будет собрана
                article_link = card.attrib.get("href")
                title = card.css("h5::text").get()
                yield response.follow(article_link, callback=self.parse_article, meta={
                    "grid_url": response.url,
                    "title": title,
                    "date": article_date
                })

    def parse_article(self, response):
        item = ArticleItem()
        grid_url = response.meta['grid_url']
        item['date'] = response.meta['date']
        item['title'] = response.meta['title']
        item['url'] = response.url
        article_content = [text.strip() for text in response.xpath("//article//p[not(@*)]/text()").getall()]

        item['content'] = '\n'.join(article_content)

        yield item
        yield Request(grid_url, callback=self.parse)
