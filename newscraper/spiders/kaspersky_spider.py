from newscraper.basic_spider import BasicSpider
from ..items import Article
import os
import re
from datetime import datetime, timedelta, timezone
import locale
# locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
import dateparser
from scrapy import Request

class KasperskySpider(BasicSpider):
    name = 'kaspersky'
    allowed_domains = ['kaspersky.ru']
    start_urls = ['https://www.kaspersky.ru/about/press-releases?sub=03%3A%3AНовости%20о%20киберугрозах']

    def parse(self, response):
        timeframe = int(os.getenv("TIMEFRAME", '7'))
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=timeframe)

        for card in response.css("div[class^='ArticleGrid_grid_'] div[data-at-selector='media-card']"):
            article_date = card.css("span[data-date]::text").get()
            article_date = dateparser.parse(article_date, languages=['ru']).replace(tzinfo=timezone.utc)

            if article_date >= cutoff_date: # статья "старше" чем  не будет собрана
                article_link = card.css("h3 a::attr(href)").get()
                title = card.css("h3 a::text").get()
                summary = card.css("span[data-summary]::text").get()
                yield response.follow(article_link, callback=self.parse_article, meta={
                    "grid_url": response.url,
                    "title": title,
                    "summary": summary,
                    "date": article_date
                })


    def parse_article(self, response):
        item = Article()
        grid_url = response.meta['grid_url']
        item['title'] = response.meta['title']
        item['summary'] = response.meta['summary']
        item['date'] = response.meta['date']
        item['url'] = response.url
        article_content = [text.replace("\\t", " ").replace("\\n", " ") for text in response.css("div[class^='ArticleBody_content_']").xpath("string()").getall()]
        article_content = [re.sub(r'\s+', ' ', text).strip() for text in article_content]

        item['content'] = '\n'.join(article_content)

        yield item
        yield Request(grid_url, callback=self.parse)

        
