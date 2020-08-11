# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    news_id = scrapy.Field()
    doc_type = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    pass
