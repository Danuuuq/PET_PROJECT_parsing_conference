# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserConferenceItem(scrapy.Item):
    id = scrapy.Field()
    date = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    room = scrapy.Field()
    comment = scrapy.Field()
    organizer = scrapy.Field()
    manager = scrapy.Field()
    after_call = scrapy.Field()
