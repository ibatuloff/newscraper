# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ArticleItem(Item):
    url = Field()
    title = Field()
    content = Field()
    date = Field()
    author = Field() # опционально
    topic = Field() # опционально
    summary = Field() # есть не на всех сайтах, опционально


    
    
