from newscraper.basic_spider import BasicSpider
from newscraper.items import ArticleItem
import os
import re
from datetime import datetime, timedelta, timezone
import dateparser
from scrapy import Request

class SecurityVesionSpider(BasicSpider):
    name = 'securityvision'
    allowed_domains = ['securityvision.ru']
    site_url = 'https://www.securityvision.ru'
    site_name = 'securityvision.ru'
    start_urls = ['https://www.securityvision.ru/news']

    def parse(self, response):
        timeframe = int(os.getenv("TIMEFRAME", '7'))
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=timeframe)
        cards = response.css("div[class='news-main-article__col']")
        last_article_date = None
        page_num = response.meta.get("page_num", 1)
        for i, card in enumerate(cards):
            article_date = card.css("span[class='date']::text").get()
            article_date = dateparser.parse(article_date, languages=['ru']).replace(tzinfo=timezone.utc)
            if article_date <= cutoff_date: # статья "старше" чем  не будет собрана
                last_article_date = article_date
                article_link = card.css("a[class='post-link']").attrib.get("href")
                title = card.css("div[class='news-header'] h3::text").get()
                yield response.follow(article_link, callback=self.parse_article, meta={
                    "grid_url": response.url,
                    "title": title,
                    "date": article_date
                })
        # ленивая подгрузка контента. Выполняется если последняя статья в списке cards была не старше чем cutoff_date
        if last_article_date <= cutoff_date:
            page_num += 1
            yield response.follow(
                "https://www.securityvision.ru/news/?PAGEN_3={page_num}",
                callback=self.parse,
                meta={
                    "page_num": page_num
                }
            )

    def parse_article(self, response):
        item = ArticleItem()
        grid_url = response.meta['grid_url']
        item['title'] = response.meta['title']
        item['date'] = response.meta['date']
        item['url'] = response.url
        article_content = [text.strip() for text in response.css("div[class^='ArticleBody_content_']").xpath("string()").getall()]
        item['content'] = '\n'.join(article_content)

        yield item
        yield Request(grid_url, callback=self.parse)
