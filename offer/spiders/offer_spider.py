import string
import re
import logging
from datetime import datetime
from scrapy.spiders import Spider
from scrapy.selector import Selector
from offer.items import TescoOfferItem
from offer.items import SainsburysOfferItem
import requests
import lxml.html
import math
from urllib.parse import urlsplit, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

logger = logging.getLogger()
class AsdaOfferSpider(Spider):
    name = "asdaoffer"
    allowed_domains = ["asda.com"]
    start_urls = getAsdaStartUrl()

    def parse(self, response):
        hxs = Selector(response) # The XPath selector
        product_grid='//div[@id="productsContainer"]/div[@id="productLister"]/ul[contains(@class,"productLister")]//li[@class="gridItem"]'
        product_id_tag='.//div[@class="productInfo"]//div[@class="promotion"]//a/@href'
        offer_desc_tag='.//div[@class="productInfo"]//div[@class="promotion"]//a/text()'
        product_url='.//div[@class="productInfo"]//h3/a/@href'
        product_desc_tag='.//div[@class="productInfo"]//h3/a/text()'
        product_imgsrc_tag='.//div[@class="productInfo"]//h3/a/img/@src'
        offertags = hxs.xpath(product_grid)
        sainsoffers = []
        logging.info(len(offertags))

        for offertag in offertags:
            offer = SainsburysOfferItem()
            logging.debug(offertag)
            offer['productid'] = parse_qs(urlsplit(offertag.xpath(product_id_tag).extract()[0]).query)['productId'][0]
            offer['imgsrcl'] = offertag.xpath(product_imgsrc_tag).extract()[0]
            offer['productdesc'] = offertag.xpath(product_desc_tag).extract()[0].replace('  ','').replace('\r\n','')
            offer['offerdesc'] = offertag.xpath(offer_desc_tag).extract()[0].replace('  ','').replace('\r\n','')
            offer['producturl'] = offertag.xpath(product_url).extract()[0]
            sainsoffers.append(offer)
        return sainsoffers


class TescoOfferSpider(Spider):
    name = "tescooffer" # Name of the spider, to be used when crawling
    allowed_domains = ["tesco.com"] # Where the spider is allowed to go
    start_urls = getTescoStartUrl()

    def parse(self, response):
        hxs = Selector(response) # The XPath selector

        # XPath Tags
        productlist_tag = '//div[@class="product-lists"]//ul[@class="product-list grid"]/li'
        product_id_tag = './/div[@class="product-tile--wrapper"]//div[@class="tile-content"]/a/@href'
        product_imgsrc_tag = './/img/@src'
        product_desc_tag = './/div[@class="product-details--wrapper"]//a/text()'
        offer_desc_tag = './/li[@class="product-promotion"]//span[@class="offer-text"]/text()'
        validity_desc_tag = './/li[@class="product-promotion"]//span[@class="dates"]/text()'
        offertags = hxs.xpath(productlist_tag)
        ###

        tescooffers = []
        for offertag in offertags:
            offer = TescoOfferItem()
            offer['productid'] = offertag.xpath(product_id_tag).extract()[0].replace("/groceries/en-GB/products/","")
            if offertag.xpath(product_imgsrc_tag).extract():
                offer['imgsrc225'] = offertag.xpath(product_imgsrc_tag).extract()[0]
                offer['imgsrc110'] = offertag.xpath(product_imgsrc_tag).extract()[0].replace('225x225','110x110')
                offer['imgsrc90'] = offertag.xpath(product_imgsrc_tag).extract()[0].replace('225x225','90x90')
                offer['imgsrc540'] = offertag.xpath(product_imgsrc_tag).extract()[0].replace('225x225','540x540')
            else:
                offer['imgsrc90'] = ""
                offer['imgsrc540'] = ""
                offer['imgsrc110'] = ""
                offer['imgsrc225'] = ""
            if offertag.xpath(product_desc_tag).extract():
                offer['productdesc'] = offertag.xpath(product_desc_tag).extract()[0]
            else:
                offer['productdesc'] = ""
            if offertag.xpath(offer_desc_tag).extract():
                offer['offerdesc'] = offertag.xpath(offer_desc_tag).extract()[0]
            else:
                offer['offerdesc'] = ""
            if offertag.xpath(validity_desc_tag).extract():
                offer['validitydesc'] = offertag.xpath(validity_desc_tag).extract()[0]
            else:
                offer['validitydesc'] = ""
            tescooffers.append(offer)
        return tescooffers # To be changed later

class SainsOfferSpider(Spider):
    name = "sainsoffer" # Name of the spider, to be used when crawling
    allowed_domains = ["sainsburys.co.uk"] # Where the spider is allowed to go
    start_urls = getSainsStartUrl()

    def parse(self, response):
        hxs = Selector(response) # The XPath selector
        product_grid='//div[@id="productsContainer"]/div[@id="productLister"]/ul[contains(@class,"productLister")]//li[@class="gridItem"]'
        product_id_tag='.//div[@class="productInfo"]//div[@class="promotion"]//a/@href'
        offer_desc_tag='.//div[@class="productInfo"]//div[@class="promotion"]//a/text()'
        product_url='.//div[@class="productInfo"]//h3/a/@href'
        product_desc_tag='.//div[@class="productInfo"]//h3/a/text()'
        product_imgsrc_tag='.//div[@class="productInfo"]//h3/a/img/@src'
        offertags = hxs.xpath(product_grid)
        sainsoffers = []
        logging.info(len(offertags))

        for offertag in offertags:
            offer = SainsburysOfferItem()
            logging.debug(offertag)
            offer['productid'] = parse_qs(urlsplit(offertag.xpath(product_id_tag).extract()[0]).query)['productId'][0]
            offer['imgsrcl'] = offertag.xpath(product_imgsrc_tag).extract()[0]
            offer['productdesc'] = offertag.xpath(product_desc_tag).extract()[0].replace('  ','').replace('\r\n','')
            offer['offerdesc'] = offertag.xpath(offer_desc_tag).extract()[0].replace('  ','').replace('\r\n','')
            offer['producturl'] = offertag.xpath(product_url).extract()[0]
            sainsoffers.append(offer)
        return sainsoffers
