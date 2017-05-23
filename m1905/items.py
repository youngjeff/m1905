# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class M1905Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    info_id = scrapy.Field()
    name = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()
    type = scrapy.Field()
    country = scrapy.Field()
    date = scrapy.Field()
    gernic = scrapy.Field()
    score = scrapy.Field()
    time = scrapy.Field()