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

class TescoOfferSpider(Spider):

    #def gettescooffercount(self):
    r  = requests.get('https://www.tesco.com/groceries/en-GB/promotions/alloffers')
    data = lxml.html.fromstring(r.text)
    output = data.xpath('//span[@class="items-count-filter-caption"]/text()')
    itemcount = output[0].split(' ')
    print(math.ceil(int(itemcount[0])/24))
    #    return math.ceil(int(itemcount[0])/24)

    name = "tescooffer" # Name of the spider, to be used when crawling
    allowed_domains = ["tesco.com"] # Where the spider is allowed to go

    maxpage = math.ceil(int(itemcount[0])/24)

    start_urls = [
        'https://www.tesco.com/groceries/en-GB/promotions/alloffers?page=%d' % (n) for n in range(1,maxpage)
    ]        
	
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

    #def build_starturl():
    categoryId=[12518,13343,267396,267397,12320,218831,12422,12192,12448,11651,12564,12298,281806]
    #categoryId=[12518]
    #categoryId=[12518,13343,12422]
    urlstring='https://www.sainsburys.co.uk/shop/gb/groceries/home/CategorySeeAllView?langId=44&storeId=10151&catalogId=10123&pageSize=108&facet=88&categoryId=%d&categoryFacetId1=%d&beginIndex=%d'
    start_url = []
    for n in categoryId:
        r  = requests.get(urlstring%(n,n,0))
        data = lxml.html.fromstring(r.text)
        output = data.xpath('//h1[@id="resultsHeading"]/text()')
        item = output[0].replace('  ','').replace('\r\n','').split('(')[0]
        itemcount = output[0].replace('  ','').replace('\r\n','').split('(')[1].split(' ')[0]
        print(item,':',itemcount)
        for i in range(0,math.ceil(int(itemcount.replace(',',''))/108)):
            start_url.append(urlstring%(n,n,i*108))
            print(urlstring%(n,n,i*108))
    #    return start_url

    start_urls = start_url

    #start_urls = [
    #    'https://www.sainsburys.co.uk/shop/gb/groceries/home/CategorySeeAllView?langId=44&storeId=10151&catalogId=10123&pageSize=108&beginIndex=0&facet=88&categoryId=%d&categoryFacetId1=%d' % (n,n) for n in categoryId
    #]

    def parse(self, response):
        hxs = Selector(response) # The XPath selector
        product_grid='//div[@id="productsContainer"]/div[@id="productLister"]/ul[contains(@class,"productLister")]//li[@class="gridItem"]'
        product_id_tag='.//div[@class="productInfo"]//div[@class="promotion"]//a/@href'
        offer_desc_tag='.//div[@class="productInfo"]//div[@class="promotion"]//a/text()'
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
            sainsoffers.append(offer)
        return sainsoffers