# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy, re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class WishNewItem(scrapy.Item):
    is_new = scrapy.Field()
    goods_name = scrapy.Field()
    sale_num = scrapy.Field()
    default_img = scrapy.Field()
    list_img = scrapy.Field()
    introduce = scrapy.Field()
    source_id = scrapy.Field()
    url = scrapy.Field()
    tags = scrapy.Field()
    create_time = scrapy.Field()
    enabled = scrapy.Field()
    price = scrapy.Field()
    shipping = scrapy.Field()
    msrp = scrapy.Field()
    variation_id = scrapy.Field()
    merchant_id = scrapy.Field()
    merchant_name = scrapy.Field()
    size_id = scrapy.Field()
    color_id = scrapy.Field()
    extra_photo_sequence_id = scrapy.Field()
    keywords = scrapy.Field()
    num_wishes = scrapy.Field()
    average_score = scrapy.Field()
    rating_count = scrapy.Field()
    currently_viewing_nums = scrapy.Field()
    rating_size_num = scrapy.Field()
    rating_size_summary = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    INSERT INTO wish_new_item(%s)
                    VALUES ({0})
                    """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class WishProductItem(WishNewItem):
    def get_insert_sql(self):
        insert_sql = """
                            INSERT INTO wish_item_log(%s)
                            VALUES ({0})
                            """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class WishSkuNewItem(scrapy.Item):
    source_id = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    enabled = scrapy.Field()
    variantId = scrapy.Field()
    price = scrapy.Field()
    msrp = scrapy.Field()
    shippingPrice = scrapy.Field()
    main_image = scrapy.Field()
    extra_photo_sequence_id = scrapy.Field()
    create_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    INSERT INTO wish_new_item_sku(%s)
                    VALUES ({0})
                    """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class WishProductSkuItem(WishSkuNewItem):
    def get_insert_sql(self):
        insert_sql = """
                            INSERT INTO wish_item_sku_log(%s)
                            VALUES ({0})
                            """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


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
                REPLACE INTO fetch_xiciproxy(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class TakeFirstLoader(ItemLoader):
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
    status = scrapy.Field()
    date_uploaded=scrapy.Field()
    categoryId= scrapy.Field()
    dangerousKind=scrapy.Field()

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
    status = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO item_sku_log(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class JoomCateProductItem(JoomProductItem):
    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO joom_cate_product(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class JoomCateSkuItem(JoomSkuItem):
    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO joom_cate_sku(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params

class JoomTmpProductItem(JoomProductItem):
    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO joom_tmp_product(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class JoomTmpSkuItem(JoomSkuItem):
    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO joom_tmp_sku(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class ShopeeItem(scrapy.Item):
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
    rating_count = scrapy.Field()
    average_score = scrapy.Field()
    cate = scrapy.Field()
    source_id = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    storeId = scrapy.Field()
    price_min = scrapy.Field()
    price_max = scrapy.Field()
    date_uploaded = scrapy.Field()
    is_official_shop = scrapy.Field()
    sold = scrapy.Field()
    currency = scrapy.Field()
    liked_count = scrapy.Field()
    stock = scrapy.Field()
    is_hot_sales = scrapy.Field()
    item_status = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO shopee_item(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class ShopeeSkuItem(scrapy.Item):
    source_id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    msrp = scrapy.Field()
    main_image = scrapy.Field()
    create_time = scrapy.Field()
    variantId = scrapy.Field()
    stock = scrapy.Field()
    currency = scrapy.Field()
    status = scrapy.Field()
    sold = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    INSERT INTO shopee_sku_item(%s)
                    VALUES ({0})
                    """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class FMItem(scrapy.Item):
    goods_name = scrapy.Field()
    price = scrapy.Field()
    msrp = scrapy.Field()
    sale_num = scrapy.Field()
    default_img = scrapy.Field()
    list_img = scrapy.Field()
    introduce = scrapy.Field()
    rating_count = scrapy.Field()
    average_score = scrapy.Field()
    cate = scrapy.Field()
    source_id = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    storeId = scrapy.Field()
    date_uploaded = scrapy.Field()
    updatedAt = scrapy.Field()
    tags = scrapy.Field()
    priceEuro = scrapy.Field()
    msrpEuro = scrapy.Field()
    shippingCost = scrapy.Field()
    shippingCostEuro = scrapy.Field()
    brand = scrapy.Field()
    sku = scrapy.Field()
    msku = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO fm_item(%s)
                VALUES ({0})
                """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class FMSkuItem(scrapy.Item):
    source_id = scrapy.Field()
    price = scrapy.Field()
    msrp = scrapy.Field()
    create_time = scrapy.Field()
    variantId = scrapy.Field()
    stock = scrapy.Field()
    status = scrapy.Field()
    active = scrapy.Field()
    priceEuro = scrapy.Field()
    msrpEuro = scrapy.Field()
    shippingCost = scrapy.Field()
    shippingCostEuro = scrapy.Field()
    sourceShippingCost = scrapy.Field()
    sourcePrice = scrapy.Field()
    msku = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    INSERT INTO fm_sku_item(%s)
                    VALUES ({0})
                    """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


def extract_us(value):
    return re.match('.*\s(\d.*$)', value).group(1)


def extract_merchant_id(value):
    return value.strip('/').split('merchant-')[-1]


def handle_image(value):
    return ('https:' + value).replace('150_150', '500_500')


class VovaItem(scrapy.Item):
    goods_name = scrapy.Field()
    price = scrapy.Field(
        input_processor=MapCompose(extract_us)
    )
    msrp = scrapy.Field(
        input_processor=MapCompose(extract_us)
    )
    default_img = scrapy.Field(
        input_processor=MapCompose(handle_image)
    )
    list_img = scrapy.Field(
        input_processor=MapCompose(handle_image),
        output_processor=Join('|')
    )
    introduce = scrapy.Field()
    cate = scrapy.Field()
    source_id = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    storeId = scrapy.Field(
        input_processor=MapCompose(extract_merchant_id)
    )

    def get_insert_sql(self):
        insert_sql = """
                    INSERT INTO vova_item(%s)
                    VALUES ({0})
                    """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class VovaSkuItem(scrapy.Item):
    source_id = scrapy.Field()
    price = scrapy.Field()
    msrp = scrapy.Field()
    main_image = scrapy.Field()
    create_time = scrapy.Field()
    variantId = scrapy.Field()
    stock = scrapy.Field()
    shipping_cost = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    INSERT INTO vova_sku_item(%s)
                    VALUES ({0})
                    """ % (','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params
