# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class OfferItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	productid = Field()
	imgsrc90 = Field()
	imgsrc110 = Field()
	imgsrc540 = Field()
	imgsrc225 = Field()
	productdesc = Field()
	offerdesc = Field()
	validitydesc = Field()
	offerStart = Field()
	offerEnd = Field()
