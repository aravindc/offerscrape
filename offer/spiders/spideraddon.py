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

def getAsdaStartUrl():
    asda_start_url = []
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('window-size=1200x600')
    offerurl = 'https://groceries.asda.com/special-offers/all-offers/by-category/'
    asdaurl = 'https://groceries.asda.com/special-offers/all-offers/by-category/%s?No=%d'
    categories = '{"Fresh Food & Bakery": "103099"}'
    #categories = '{"Fresh Food & Bakery": "103099", "Chilled Food": "111621", "Food Cupboard":"102870","Frozen Food":"103478","Drinks":"102436","Health & Beauty":"103605","Laundry & Household":"104074","Baby, Toddler & Kids":"102269","Home & Entertainment":"102592","Pets":"111556"}'
    json_cat = json.loads(categories)
    asda_start_url = []
    for onecat in json_cat:
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(offerurl+json_cat[onecat])
        itemcount = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH,'//div/p[contains(@class,"itemCount specialoffers")]/strong')))
        totalproducts = itemcount[2].text
        totalpages = math.ceil(int(int(totalproducts)/15))
        driver.quit()
        print("asda offers: %s - %d" % (json_cat[onecat],totalpages))
        for i in range(0,totalpages):
            asda_start_url.append(asdaurl%(json_cat[onecat],i*15))
            #print(asdaurl%(json_cat[onecat],i*15))
    print(asda_start_url)
    return asda_start_url

def getTescoStartUrl():
    tesco_start_url = []
    r  = requests.get('https://www.tesco.com/groceries/en-GB/promotions/alloffers')
    data = lxml.html.fromstring(r.text)
    #output = data.xpath('//span[@class="items-count-filter-caption"]/text()')
    output = data.xpath('//div[@class="items-count__filter-caption"]//text()')
    itemcount = output[3].split(' ')
    print(math.ceil(int(itemcount[0])/24))
    #    return math.ceil(int(itemcount[0])/24)
    maxpage = math.ceil(int(itemcount[0])/24)
    tescourl = 'https://www.tesco.com/groceries/en-GB/promotions/alloffers?page=%d'
    for i in range(1,maxpage):
        tesco_start_url.append(tescourl % i)
    return tesco_start_url

def getSainsStartUrl():
    sains_start_url = []
    #def build_starturl():
    #categoryId=[12518,13343,267396,267397,12320,218831,12422,12192,12448,11651,12564,12298,281806]
    categoryId=[12518]
    #categoryId=[12518,13343,12422]
    urlstring='https://www.sainsburys.co.uk/shop/gb/groceries/home/CategorySeeAllView?langId=44&storeId=10151&catalogId=10123&pageSize=108&facet=88&categoryId=%d&categoryFacetId1=%d&beginIndex=%d'
    for n in categoryId:
        r  = requests.get(urlstring%(n,n,0))
        data = lxml.html.fromstring(r.text)
        output = data.xpath('//h1[@id="resultsHeading"]/text()')
        item = output[0].replace('  ','').replace('\r\n','').split('(')[0]
        itemcount = output[0].replace('  ','').replace('\r\n','').split('(')[1].split(' ')[0]
        print(item,':',itemcount)
        for i in range(0,math.ceil(int(itemcount.replace(',',''))/108)):
            sains_start_url.append(urlstring%(n,n,i*108))
            print(urlstring%(n,n,i*108))
    return sains_start_url
