# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyBaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PipelineBasedSavedItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    breadcrumbs = scrapy.Field()
    price = scrapy.Field()
    price2 = scrapy.Field()
    parameters = scrapy.Field()
    categories = scrapy.Field()
    exhibitions = scrapy.Field()
    details = scrapy.Field()
