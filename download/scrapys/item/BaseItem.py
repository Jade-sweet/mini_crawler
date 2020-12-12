# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyItem(scrapy.Item):
    fields = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattr__(self, name):
        return self._values[name]

    def __setattr__(self, name, value):
        super(scrapy.Item, self).__setattr__(name, value)

    def __setitem__(self, key, value):
        if key in self.fields:
            self._values[key] = value
