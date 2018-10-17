# -*- coding:UTF-8 -*-
import os,sys
import pickle,redis
import django

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE']='joom_scrapy.settings'
django.setup()
from fetch.models import ItemUrl

client = redis.StrictRedis('122.226.65.250',18003)


ItemUrl.objects.filter(state=0).update(state=1)
for item in ItemUrl.objects.filter(state=1).values('url_str'):
    client.lpush('joom:start_urls',pickle.dumps(item['url_str']))


