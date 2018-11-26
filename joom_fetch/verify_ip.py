# -*- coding:UTF-8 -*-
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
import gevent
import os, sys, datetime
import django,time
import requests

django_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(django_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'joom_scrapy.settings'
django.setup()

verify_url = 'https://api.joom.com/1.1/users/self/preferences?currency=USD&language=en-US&_=jomoqtns'
# headers = {
#     'origin': "https://www.joom.com",
#     'referer': "https://www.joom.com/en",
#     'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
#     'x-api-token': "Zq6Nk6Ks9XP32c0V3CCjTVHzuGw2wsap",
#     'x-version': "0.3.2"
# }

from fetch.models import XiciProxy


def react_request(item):
    proxies = {item.protocol: "%s://%s:%s" % (item.protocol, item.ip, item.port)}
    print('request %s' % item.id)
    try:

        r = requests.options(verify_url, proxies=proxies, timeout=20, allow_redirects=False)

        if r.status_code == 200:
            print('success')
            item.available = True
            item.check_time = datetime.datetime.now()
            item.joom_response_time = r.elapsed.microseconds / 1000000
            # item.joom_access_token=r.json()['payload']['accessToken']
            item.save()
        else:
            print('transparent')
            item.available = False
            item.save()
    except:
        print('failure')
        item.available = False
        item.save()


# get_url = 'https://www.joom.com/tokens/init?_=jomyko6d'
get_url = 'http://122.226.65.250:18850'
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}


def get_access_token(item):
    proxies = {item.protocol: "%s://%s:%s" % (item.protocol, item.ip, item.port)}
    print('request %s' % item.id)
    try:
        r = requests.get(get_url, proxies=proxies, allow_redirects=False,timeout=200)
        if r.text!='125.112.217.187':
            print('success')
    except:
        print('failure')


# for item in XiciProxy.objects.all():
#     react_request(item)
# proxy=[]
# for item in XiciProxy.objects.filter(available__isnull=False):
#     proxy.append("%s://%s:%s" % (item.protocol, item.ip, item.port))
# print(proxy)
# react_request(XiciProxy.objects.all()[0])
p=Pool(40)
p.map(get_access_token,XiciProxy.objects.all())
p.join()
p.kill()
