# -*- coding:UTF-8 -*-
import os,sys
import redis
import django


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE']='joom_scrapy.settings'
django.setup()
from fetch.models import ItemUrl,WishShop,Shop,WishCrawlProduct

client = redis.StrictRedis('122.226.65.250',18003)

#
ItemUrl.objects.filter(state=0).update(state=1)
for item in ItemUrl.objects.filter(state=1).values('url_str'):
    client.lpush('joom:start_urls',item['url_str'])
# WishShop.objects.filter(state__lt=600).update(state=1)
# for url in WishShop.objects.filter(state=1).values('url'):
#     client.lpush('wish:start_urls',url['url'])
#
# Shop.objects.filter(platform_id=9,status__lt=3).update(status=1)
# for token in Shop.objects.filter(platform_id=9,status=1).values('access_token','id'):
#     client.lpush('wish_api:start_urls', '%s+%s' %(token['id'],token['access_token']))

#
# for wish_product in WishCrawlProduct.objects.all():
#     client.lpush('wish_rating:start_urls',wish_product.source_id)
