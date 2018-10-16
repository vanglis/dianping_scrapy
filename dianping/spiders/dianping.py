# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from bs4 import BeautifulSoup
from dianping.items import CategoryItem,ShopItem,ShopInfomationItem
from urllib.parse import urlparse
import requests
import re
import time
import json

class DianpingspiderSpider(scrapy.Spider):
    name = "dianping"
    allowed_domains = ["dianping.com"]
    #start_urls = ['http://www.dianping.com/shanghai/ch10/g101']
    start_urls = ['shanghai']
    #start_urls = ['shanghai', 'beijing']
    def __init__(self):
        self.list_url = 'http://www.dianping.com/shanghai/ch10/g101'
        self.cookies = {'dper':'4d35f8c329a67b456b4cdb53231182a683608509f603067ec13ef3f7ec39203ee86c36302c44282ed2fe10bb8b9197214c047d0625e661d3912451ccb4f8208a38a5c938150381d9f7eeffddb172c3b1fe3ce8a67ae70b281621e5ec8371140e'}
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}

    def start_requests(self):
        while self.start_urls.__len__():
            city = self.start_urls.pop()
            url_index = "http://www.dianping.com/%s" % city
            yield scrapy.Request(url_index, callback=self.parse0)
        #
        # for u in self.start_urls:
        #     yield scrapy.Request(u, cookies=self.cookies, callback=self.parse)


    def parse0(self, response):
        """抓取分类列表页链接"""
        categoryItem = CategoryItem()
        categoryItem["urlCategoryFood"] = response.xpath(".//a[@data-category='index.food']/@href").extract()
        categoryItem["urlCategoryLife"] = response.xpath(".//a[@data-category='index.life']/@href").extract()
        categoryItem["urlCategoryWedding"] = response.xpath(".//a[@data-category='index.wedding']/@href").extract()
        categoryItem["urlCategoryMovie"] = response.xpath(".//a[@data-category='index.movie']/@href").extract()
        categoryItem["urlCategoryBeauty"] = response.xpath(".//a[@data-category='index.beauty']/@href").extract()
        categoryItem["urlCategoryHotel"] = response.xpath(".//a[@data-category='index.hotel']/@href").extract()
        categoryItem["urlCategoryBaby"] = response.xpath(".//a[@data-category='index.baby']/@href").extract()
        categoryItem["urlCategoryView"] = response.xpath(".//a[@data-category='index.view']/@href").extract()
        categoryItem["urlCategorySports"] = response.xpath(".//a[@data-category='index.sports']/@href").extract()
        categoryItem["urlCategoryShopping"] = response.xpath(".//a[@data-category='index.shopping']/@href").extract()
        categoryItem["urlCategoryHome"] = response.xpath(".//a[@data-category='index.home']/@href").extract()
        categoryItem["urlCategoryEducation"] = response.xpath(".//a[@data-category='index.education']/@href").extract()
        categoryItem["urlCategoryOther"] = response.xpath(".//a[@data-category='index.other']/@href").extract()
        categoryItem["urlCategoryMedical"] = response.xpath(".//a[@data-category='index.medical']/@href").extract()
        categoryItem["urlCategoryCar"] = response.xpath(".//a[@data-category='index.car']/@href").extract()
        urlCategorys = set() #记录待爬列表页url
        finish_urlCategorys = set() #记录已爬列表页url
        for value in categoryItem.values():
            for i in value:
                pattern = re.compile("http://www.dianping.com/(.*?)/ch(.*?)/g(.*?)", re.S)
                urlCategory = pattern.findall(i)
                if urlCategory:
                    urlCategorys.add(i)
        for urlCategory in urlCategorys:
            yield scrapy.Request(url=urlCategory, callback=self.parse1)
        yield categoryItem


    def parse1(self, response):
        shopItem = ShopItem()
        shopurls = response.xpath(".//a[@class='shopname']/@href").extract()
        print(shopurls)
        for shopurl in shopurls :
            urlpath = urlparse(shopurl).path
            urlpath_list = urlpath.split('/')
            shopid = urlpath_list[2]
            shop_detailapi = 'http://www.dianping.com/ajax/json/shopDynamic/reviewAndStar?shopId={shopid}&cityId=1&mainCategoryId=116&_token=eJx1T8tOwzAQ%2FJc9W7Hd2LGJxKEvoIUUKQ1BUPVgkpJYkDSNI9IW8e9sRTlwQFppHjsa7X5CO8sh5IwxwQl8bFoIgXvMC4BA53AjB1r6SgaC%2B5pA9teTviDw0qYTCFdaKKI0W5%2BMGPWKC8HIBUPnh2ql1mQgcE6ZGUag7LompLTvey%2B3pm5sXXjZtqKu3DY04FpIxvCQ%2F2OmLkpjaVZyBthaJdiK%2BHZGc8buV0f4HhY6W9TINvN9snTC7V7jyCXpw4H50fFmcX83fV8cD3o83luzi9NajrJh9Wiur6ypRsXz7XCq5pP86RK%2BvgGAxFs4&uuid=5e1b57b5-5aa8-f895-665c-018d847a34b2.1527410439&platform=1&partner=150&originUrl=http%3A%2F%2Fwww.dianping.com%2Fshop%2F{shopid}'.format(shopid = shopid)
            yield scrapy.Request(url = shop_detailapi, cookies = self.cookies, callback=self.parse2)
            shopItem["shopid"] = shopid
            shopItem["shop_url"] = shopurl
            yield shopItem

        # print(urlparse(response.url).netloc)
        # print(response.xpath('//a[@class="next"]/@href').extract())
        # if urlparse(response.url).netloc == 'verify.meituan.com' :
        #     self.driver.get(response.url)
        #     print('等待输入验证码。。。')
        #     yzm = input('确认验证码是否输入完毕，1为ok：')
        #     if yzm == '1' :
        #         scrapy.Request(url=self.next_url, cookies=self.cookies, dont_filter=True, callback=self.parse)
        #     else:
        #         print('error')
        # elif response.xpath('//a[@class="next"]/@href').extract() :
        #     self.next_url = response.xpath('//a[@class="next"]/@href').extract()[0]
        #     print(self.next_url)
        #     yield scrapy.Request(url=self.next_url, cookies=self.cookies, dont_filter=True, callback=self.parse2)
        # else:
        #     print("没有下一页了")

    def parse2(self, response):
        shopInfomationItem = ShopInfomationItem()
        print(response.body)