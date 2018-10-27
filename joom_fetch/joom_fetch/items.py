# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from fetch.models import ItemLog, XiciProxy, WishCrawlProduct, WishVariantItem
from scrapy_djangoitem import DjangoItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


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


class XiciDeferItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    address = scrapy.Field()
    protocol = scrapy.Field(
        input_processor=MapCompose(str.lower)
    )
    available = scrapy.Field()
    create_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                REPLACE INTO xici(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class XiciLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JoomProductItem(scrapy.Item):
    goods_name = scrapy.Field()
    price = scrapy.Field()
    msrp = scrapy.Field()
    sale_num = scrapy.Field()
    default_img = scrapy.Field()
    list_img = scrapy.Field()
    introduce = scrapy.Field()
    score1 = scrapy.Field()
    score2 = scrapy.Field()
    score3 = scrapy.Field()
    score4 = scrapy.Field()
    score5 = scrapy.Field()
    average_score = scrapy.Field()
    cate = scrapy.Field()
    source_id = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    storeId = scrapy.Field()
    tags = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO item_log(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class JoomStoreItem(scrapy.Item):
    storeId = scrapy.Field()
    updatedTimeMerchantMs = scrapy.Field()
    enabled = scrapy.Field()
    enabledByMerchant = scrapy.Field()
    rating = scrapy.Field()
    name = scrapy.Field()
    positiveReviewsCount = scrapy.Field()
    favoritesCount = scrapy.Field()
    productsCount = scrapy.Field()
    reviewsCount = scrapy.Field()

    def get_insert_sql(self):
        """
            REPLACE INTO:如果发现表中已经有此行数据（根据主键或者唯一索引判断）则先删除此行数据，然后插入新的数据
        """
        insert_sql = """
                REPLACE INTO joom_stroe(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class JoomSkuItem(scrapy.Item):
    source_id = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    price = scrapy.Field()
    msrp = scrapy.Field()
    main_image = scrapy.Field()
    create_time = scrapy.Field()
    variantId = scrapy.Field()
    inStock = scrapy.Field()
    createdTimeMs = scrapy.Field()
    publishedTimeMs = scrapy.Field()
    shippingPrice = scrapy.Field()
    shippingWeight = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO item_sku_log(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params
