# -*- coding:UTF-8 -*-
import os,sys
import pickle,redis
import django

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE']='joom_scrapy.settings'
django.setup()
from fetch.models import ItemUrl

client = redis.StrictRedis('122.226.65.250',18003)

for item in ItemUrl.objects.filter(state=0):
    client.lpush('joom:start_urls',pickle.dumps(item.url_str))

