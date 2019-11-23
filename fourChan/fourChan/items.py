# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class FourchanItem(Item):
    post_id = Field()
    post_content = Field()
    post_timestamp = Field()
    post_userid = Field()
    post_link = Field()
    post_replies = Field()
    post_scraped_time = Field()
    post_replies_count = Field()
    post_subject = Field()
