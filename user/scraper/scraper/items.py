# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

import scrapy

class ProductItem(scrapy.Item):
    product_name = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    condition = scrapy.Field()
    photos = scrapy.Field()
    product_url = scrapy.Field()
