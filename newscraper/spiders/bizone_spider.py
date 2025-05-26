from newscraper.basic_spider import BasicSpider
from newscraper.items import ArticleItem
import os
import re
from datetime import datetime, timedelta, timezone
import dateparser
import html

class BizoneSpider(BasicSpider):
    name = 'bizone'
    allowed_domains = ['bi.zone']
    site_url = 'https://www.bi.zone'
    site_name = 'bi.zone'
    start_urls = ['https://bi.zone/expertise/insights']

    def parse(self, response):
        timeframe = int(os.getenv("TIMEFRAME", '7'))
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=timeframe)
        cards = response.css("div[class='previewBoxWrap']")
        last_article_date = None
        page_num = response.meta.get("page_num", 1)
        for card in cards:
            article_date = card.css("div[class='previewBox__info'] time::text").get()
            article_date = dateparser.parse(article_date, languages=['ru']).replace(tzinfo=timezone.utc)
            last_article_date = article_date
            if article_date >= cutoff_date: # статья "старше" чем  не будет собрана
                article_link = card.css("div[class='previewBox__content'] a").attrib.get("href")
                title = card.css("div[class='previewBox__content'] a::text").get()
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
        article_content = [html.unescape(text).strip() for text in response.xpath("//div[contains(@class, 'sectionDefault')]//text()").getall()]
        item['content'] = '\n'.join(article_content)

        yield item
