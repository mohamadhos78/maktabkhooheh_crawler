# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaketabkhoonehItem(scrapy.Item):
    _id = scrapy.Field()
    info = scrapy.Field()
    teacher = scrapy.Field()
    category = scrapy.Field()
    time = scrapy.Field()
    price = scrapy.Field()
    organization = scrapy.Field()