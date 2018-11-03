# -*- coding:UTF-8 -*-

import pymongo
from twisted.enterprise import adbapi
from MySQLdb.cursors import DictCursor
import datetime, time, json
from decimal import Decimal
import MySQLdb
dbparams = dict(
    host='122.226.65.250',
    db='cjdn_newyiliao',
    user='cjdn_newyiliao',
    passwd='GPnGmibX6QGGzbDA',
    port=39306,
    charset='utf8mb4',
    cursorclass=DictCursor,
    use_unicode=True)
connect = MySQLdb.connect(**dbparams)
cursor = connect.cursor()
# dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)


# class WishPipeline(object):
#
#     def process_item(self, item):
#         query = dbpool.runInteraction(self.do_insert, item)
#
#         query.addErrback(self.handle_error, item)
#         return query
#
#     def do_insert(self, cursor, item):
#         insert_sql, params = item.get_insert_sql()
#         cursor.execute(insert_sql, params)
#
#     def handle_error(self, failure, item):
#         '''
#         处理异步插入数据库错误
#         :param failure:
#         :return:
#         '''
#         print(failure, item)
#
#
# wish_pipeline = WishPipeline()

def do_insert(item):
    insert_sql, params = item.get_insert_sql()
    cursor.execute(insert_sql, params)

mg = pymongo.MongoClient('122.226.65.250', 18017)
db = mg.wish_api
collection = db.shop3


class Item(dict):
    table_name = ''

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO %s(%s)
                VALUES ({0})
                """ % (self.table_name, ','.join(self.keys()))
        params = (self[i] for i in self)
        return insert_sql.format(','.join(['%s'] * len(self))), params


class WishItem(Item):
    table_name = 'wish_shop_item_s1'


class WishSkuItem(Item):
    table_name = 'wish_shop_item_sku_s1'


shops = {512, 513,514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533,
         534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 32, 33, 544, 35, 545, 546, 547, 548, 549, 550, 551, 552, 553,
         554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 567, 568, 569, 571, 570, 573, 572, 574, 575, 576,
         577, 578, 579, 580, 581, 582, 584, 583, 585, 586, 587, 588, 589, 590, 591, 593, 594, 595, 596, 597, 598, 599,
         592, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620,
         621, 622, 623, 624, 625, 628, 629, 630, 631, 632, 633, 627, 634, 635, 626, 431, 432, 434, 435, 436, 437, 438,
         439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 460, 461,
         462, 463, 464, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484,
         485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506,
         507, 508, 509, 510, 511}


def process_info(info):
    item_p = WishItem()
    item_p['goods_name'] = info['name'][:255]
    item_p['sale_num'] = int(info['number_sold'])
    item_p['default_img'] = info.get('main_image', None)
    item_p['list_img'] = info.get('extra_images', None)
    item_p['introduce'] = info['description']
    item_p['source_id'] = info['id']
    item_p['url'] = 'https://www.wish.com/product/' + info['id']
    item_p['date_uploaded'] = datetime.datetime.strptime(info['date_uploaded'], '%m-%d-%Y')
    item_p['last_updated'] = datetime.datetime.strptime(info['last_updated'], '%m-%d-%YT%H:%M:%S')
    item_p['tags'] = json.dumps(info['tags'])
    item_p['parent_sku'] = info['parent_sku']
    item_p['is_promoted'] = eval(info['is_promoted'].strip())
    item_p['review_status'] = info['review_status']
    item_p['number_saves'] = info['number_saves']
    item_p['shop_id'] = info['shop_id']
    item_p['create_time'] = int(time.time())
    variants = info['variants']
    item_p['enabled'] = any(filter(lambda x: x['Variant']['enabled'] == 'True', variants))
    min_variant = min(variants, key=lambda x: float(x['Variant']['price']))
    item_p['price'] = Decimal(min_variant['Variant']['price']).quantize(Decimal('.01'))
    item_p['msrp'] = Decimal(min_variant['Variant'].get('msrp', 0)).quantize(Decimal('.1'))
    do_insert(item_p)
    connect.commit()
    for v in variants:
        variant = v['Variant']
        sku = WishSkuItem()
        sku['source_id'] = info['id']
        sku['color'] = variant.get('color', None)
        sku['size'] = variant.get('size', None)
        sku['price'] = Decimal(variant['price']).quantize(Decimal('.01'))
        sku['enabled'] = eval(variant['enabled'].strip())
        sku['all_images'] = variant['all_images']
        sku['sku'] = variant['sku']
        sku['variantId'] = variant['id']
        sku['msrp'] = Decimal(variant.get('msrp', 0)).quantize(Decimal('.01'))
        shipping = variant.get('shipping', '').strip()
        sku['shippingPrice'] = Decimal(shipping if shipping else 0).quantize(Decimal('.01'))
        sku['shipping_time'] = variant['shipping_time']
        sku['create_time'] = int(time.time())
        do_insert(sku)
    connect.commit()
    print('product %s complete, it has %s skus' % (info['id'],len(variants)))


if __name__=='__main__':
    # dbpool.start()
    for shop in shops:
        docs = collection.find({'shop_id': shop,'number_sold':'0'})
        for info in docs:
            try:
                process_info(info)
            except:
                print(info['id']+'\r\n')
    # dbpool.close()
    connect.close()
    mg.close()
    # reactor.run()
