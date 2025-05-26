from newscraper.basic_spider import BasicSpider
from newscraper.items import ArticleItem
import os
import re
from datetime import datetime, timedelta, timezone
import dateparser
import html

class InfoTecSpider(BasicSpider):
    name = 'infotecs'
    allowed_domains = ['infotecs.ru']
    site_url = 'https://www.infotecs.ru'
    site_name = 'infotecs.ru'
    start_urls = ['https://infotecs.ru/press-center/publications']

    def parse(self, response):
        timeframe = int(os.getenv("TIMEFRAME", '7'))
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=timeframe)
        cards = response.css("div[class='b-publications-page__items'] a")
        last_article_date = None
        page_num = response.meta.get("page_num", 1)
        for card in cards:
            article_date = card.css("div[class='b-publication-item__content-date']::text").get()
            article_date = dateparser.parse(article_date, languages=['ru']).replace(tzinfo=timezone.utc)
            last_article_date = article_date
            if article_date >= cutoff_date: # статья "старше" чем  не будет собрана
                article_link = card.attrib.get("href")
                title = card.css("div[class='b-publication-item__title']::text").get()
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
        article_content = [html.unescape(text).strip() for text in response.xpath("//div[contains(@class, 'b-publications-detail-page__content')]//p//text()").getall()]
        item['content'] = '\n'.join(article_content)

        yield item
