# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from fetch.models import ItemLog,XiciProxy,WishCrawlProduct,WishVariantItem
from scrapy_djangoitem import DjangoItem


class JoomFetchItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = ItemLog


class WishShopItem(scrapy.Item):
    document = scrapy.Field()


class XiciItem(DjangoItem):
    django_model = XiciProxy


class WishProductItem(DjangoItem):
    django_model = WishCrawlProduct


class WishSkuItem(DjangoItem):
    django_model = WishVariantItem