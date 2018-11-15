# -*- coding:UTF-8 -*-
import requests, datetime
import ssl
import django, os, sys, time
from requests.exceptions import ReadTimeout, ConnectTimeout, ProxyError

this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(this_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'joom_scrapy.settings'
django.setup()
from fetch.models import XiciProxy


def print_msg(response, *args, **kwargs):
    print(response.text)


def check_proxy(item):
    proxy = {item.protocol: '%s:%s' % (item.protocol, item.ip)}
    try:
        # ssl._create_default_https_context = ssl._create_unverified_context
        r = requests.get('http://ip.ws.126.net/ipquery?ip=', timeout=3, hooks={'response': print_msg}, proxies=proxy,
                         allow_redirects=False)
        if r.status_code == 200:
            item.available = True
            item.response_time = r.elapsed.total_seconds()
        else:
            item.available = False
    except (ConnectTimeout, ReadTimeout, ProxyError):
        xici.available = False
    item.check_time = datetime.datetime.now()
    item.save()


for xici in XiciProxy.objects.all():
    delete_ports = [80, 8080]
    if xici.port in delete_ports:
        xici.delete()
    else:
        check_proxy(xici)
