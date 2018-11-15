# -*- coding:UTF-8 -*-
import os,sys
import redis
import django,datetime


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE']='joom_scrapy.settings'
django.setup()
from fetch.models import ItemUrl,WishShop,Shop,WishNewProduct,WishShopItemUrl,JoomCateInfo,JoomCateProduct

client = redis.StrictRedis('122.226.65.250',18003)


client.lpush('joom:start_urls',*ItemUrl.objects.filter(state=0).distinct().values_list('url_str',flat=True))
ItemUrl.objects.filter(state=0).update(state=1)


# for item in JoomCateProduct.objects.all().values('source_id'):
#     client.lpush('joom_tmp:start_urls',item['source_id'])
# if not client.exists('joom:start_urls'):
# ItemUrl.objects.filter(state=2).update(state=1)
# now = datetime.datetime.now()
# if now.hour==9 and now.minute<50 and not client.exists('joom:start_urls'):
#     for item in ItemUrl.objects.filter(state=1).values('url_str'):
#         client.lpush('joom:start_urls', item['url_str'])
# JoomCateInfo.objects.filter(parent_id__gt=0,state=2).update(state=1)
# for item in JoomCateInfo.objects.filter(parent_id__gt=0,state=1).values('cate_id'):
#     client.lpush('joom_cate:start_urls',item['cate_id'])


# WishShop.objects.filter(state__lt=3).update(state=1)
# for url in WishShop.objects.filter(state=1).values('url'):
#     client.lpush('wish_new_list:start_urls',url['url'])
#
# Shop.objects.filter(platform_id=9,status__lt=3).update(status=1)
# for token in Shop.objects.filter(platform_id=9,status=1).values('access_token','id'):
#     client.lpush('wish_api:start_urls', '%s+%s' %(token['id'],token['access_token']))


# for wish_product in WishNewProduct.objects.all():
#     client.lpush('wish_product_info:start_urls',wish_product.product_id)

# y=set([x['shop_id'] for x in WishShop.objects.values('shop_id')])


# for item in WishShopItemUrl.objects.filter(state=0).values('url_str'):
#     client.lpush('wish_product_info:start_urls',item['url_str'])
# WishShopItemUrl.objects.filter(state=0).update(state=1)
# print(y)

# if client.exists('wish_product_info:start_urls'):
#     for item in WishShopItemUrl.objects.filter(state=0).values('url_str'):
#         client.lpush('wish_product_info:start_urls',item['url_str'])
#     WishShopItemUrl.objects.filter(state=0).update(state=1)
# else:
#     for item in WishShopItemUrl.objects.filter(state__lt=2).values('url_str'):
#         client.lpush('wish_product_info:start_urls',item['url_str'])
#     WishShopItemUrl.objects.filter(state=0).update(state=1)