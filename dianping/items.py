# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CategoryItem(scrapy.Item):
    urlCategoryFood = scrapy.Field()
    urlCategoryLife = scrapy.Field()
    urlCategoryWedding = scrapy.Field()
    urlCategoryMovie = scrapy.Field()
    urlCategoryBeauty = scrapy.Field()
    urlCategoryHotel = scrapy.Field()
    urlCategoryBaby = scrapy.Field()
    urlCategoryView = scrapy.Field()
    urlCategorySports = scrapy.Field()
    urlCategoryShopping = scrapy.Field()
    urlCategoryHome = scrapy.Field()
    urlCategoryEducation = scrapy.Field()
    urlCategoryOther = scrapy.Field()
    urlCategoryMedical = scrapy.Field()
    urlCategoryCar = scrapy.Field()

class ShopItem(scrapy.Item):
    shopid = scrapy.Field()
    shop_url = scrapy.Field()

class ShopInfomationItem(scrapy.Item):
    shop_name = scrapy.Field()
    rank_stars = scrapy.Field()
    avgPrice = scrapy.Field()
    taste = scrapy.Field()
    environment = scrapy.Field()
    service = scrapy.Field()
    address = scrapy.Field()
    tel1 = scrapy.Field()
    tel2 = scrapy.Field()