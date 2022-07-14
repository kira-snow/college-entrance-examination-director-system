# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GaokaospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    school = scrapy.Field()
    score = scrapy.Field()
    year = scrapy.Field()
    level = scrapy.Field()
    wl = scrapy.Field()
    pass

class LinespiderItem(scrapy.Item):
    # define the fields for your item here like:
    score = scrapy.Field()
    year = scrapy.Field()
    level = scrapy.Field()
    wl = scrapy.Field()
    type = scrapy.Field()
    pass

class SegmentsItem(scrapy.Item):
    # define the fields for your item here like:
    score = scrapy.Field()
    year = scrapy.Field()
    wl = scrapy.Field()
    ranking = scrapy.Field()
    pass

class SchoolInfoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    province = scrapy.Field()
    department = scrapy.Field()
    type = scrapy.Field()
    level = scrapy.Field()
    yldx = scrapy.Field()
    ylxk = scrapy.Field()
    yjsy = scrapy.Field()
    pass