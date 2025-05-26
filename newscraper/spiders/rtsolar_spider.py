from newscraper.basic_spider import BasicSpider
from newscraper.items import ArticleItem
import os
import re
from datetime import datetime, timedelta, timezone
import dateparser
import html

class RTSolarSpider(BasicSpider):
    name = 'rtsolar'
    allowed_domains = ['rt-solar.ru']
    site_url = 'https://www.rt-solar.ru'
    site_name = 'rt-solar.ru'
    start_urls = ['https://rt-solar.ru/solar-4rays/blog']

    def parse(self, response):
        timeframe = int(os.getenv("TIMEFRAME", '7'))
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=timeframe)
        cards = response.css("article[class='blog-list__item']")
        last_article_date = None
        page_num = response.meta.get("page_num", 1)
        for card in cards:
            article_date = card.css("time::text").get()
            article_date = dateparser.parse(article_date, languages=['ru']).replace(tzinfo=timezone.utc)
            last_article_date = article_date
            if article_date >= cutoff_date: # статья "старше" чем  не будет собрана
                article_link = card.css("a[class*='link']").attrib.get("href")
                title = card.css("div[class='blog-list__text-wrapper'] p::text").get()
                yield response.follow(article_link, callback=self.parse_article, meta={
                    "grid_url": response.url,
                    "title": title,
                    "date": article_date
                })
        # ленивая подгрузка контента. Выполняется если последняя статья в списке cards была не старше чем cutoff_date
        if last_article_date >= cutoff_date:
            page_num += 1
            yield response.follow(
                f"/solar-4rays/blog/?PAGEN_2={page_num}",
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
        article_content = [html.unescape(text).strip() for text in response.xpath("//div[@class='article-body']//p[not(@*)]/text()").getall()]
        item['content'] = '\n'.join(article_content)

        yield item
