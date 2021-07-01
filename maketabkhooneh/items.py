# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaketabkhoonehItem(scrapy.Item):
    _id = scrapy.Field()
    info = scrapy.Field()
    teacher = scrapy.Field()
    duration = scrapy.Field()
    institute = scrapy.Field()
    category = scrapy.Field()
    required_time = scrapy.Field()
    price = scrapy.Field()
    full_content_access = scrapy.Field()
    organization = scrapy.Field()
    organization_email = scrapy.Field()