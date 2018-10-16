# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from bs4 import BeautifulSoup
from dianping.items import ShopInfomationItem
import re
import time
import json

class DianpingspiderSpider(scrapy.Spider):
    name = "DianPingSpider"
    allowed_domains = ["dianping.com"]
    start_urls = ['http://www.dianping.com/shanghai/ch10/g110']

    def __init__(self):
        self.driver = webdriver.Chrome()
        #self.shop_url = 'http://www.dianping.com/shop/{shop_id}'.format(shop_id = shop_id)
        self.driver.get('http://www.dianping.com')
        index = self.driver.page_source
        index_soup = BeautifulSoup(index, 'lxml')
        index_item = index_soup.find_all('a', attrs={'class': "index-item"})
        # for each_url in index_item:
        #     self.driver.get(each_url['href'])
        #     shop_list = self.driver.page_source
        #     print(shop_list)
        #     time.sleep(1)
        self.next_url = "http://www.dianping.com/shanghai/ch10/g101"



    def parse(self, response):
        item = ShopInfomationItem()


        self.driver.get(self.next_url)
        shop_list = self.driver.page_source
        list_soup = BeautifulSoup(shop_list, 'lxml')
        next_url = list_soup.find_all('a', attrs={'class': "next"})
        #print(next_url[0]['href'])
        self.next_url = next_url[0]['href']
        shop_urls = list_soup.find_all('a', attrs={'data-hippo-type': "shop"})
        print(shop_urls)
        for each_shop in shop_urls:
            self.driver.get(each_shop['href'])
            try:
                shop_detail = self.driver.page_source
            except:
                print("error")
                continue
            soup = BeautifulSoup(shop_detail, 'lxml')
            #店铺名称
            h1 = soup.body.h1.contents
            shop_name = h1[0]
            print(shop_name)

            #星级
            span = soup.find_all('span',class_ = "mid-rank-stars")
            print(span)
            rank_stars = span[0]['title']

            #人均
            avgPrice = soup.find_all('span', attrs={'id': "avgPriceTitle"})
            avgPrice = re.sub("\D", "", avgPrice[0].get_text()) #截取数字部分

            comment_score = soup.find_all('span', attrs={'id': "comment_score"})
            score = []
            for comment_score in comment_score[0]:
                score.append(comment_score)
            taste = re.findall(r'-?\d+\.?\d*e?-?\d*?', score[1].get_text()) #口味
            environment = re.findall(r'-?\d+\.?\d*e?-?\d*?', score[3].get_text())   #环境
            service = re.findall(r'-?\d+\.?\d*e?-?\d*?', score[5].get_text())   #服务

            # 地址
            address = soup.find_all('span', attrs={'itemprop': "street-address"})
            address = address[0]['title']
            print(address)

            # 电话
            tels = soup.find_all('p', attrs={'class': "expand-info tel"})
            tel_info = []
            for tel in tels[0]:
                tel_info.append(tel)
            print(len(tel_info))
            if len(tel_info) >= 7 :
                tel1 = tel_info[3].get_text()
                tel2 = tel_info[5].get_text()
            elif len(tel_info)  >= 5 and len(tel_info)  < 7:
                tel1 = tel_info[3].get_text()
                tel2 = None
            else:
                tel1 = None
                tel2 = None

            item["shop_url"] = each_shop['href']
            item["shop_name"] = shop_name
            item["rank_stars"] = rank_stars
            item["avgPrice"] = avgPrice
            item["taste"] = taste[0]
            item["environment"] = environment[0]
            item["service"] = service[0]
            item["address"] = address
            item["tel1"] = tel1
            item["tel2"] = tel2


            yield item
        print(next_url[0]['href'])
        yield scrapy.Request(url=next_url[0]['href'], dont_filter=True, callback=self.parse)