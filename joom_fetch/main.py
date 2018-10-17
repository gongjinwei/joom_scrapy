# -*- coding:UTF-8 -*-
from scrapy.cmdline import execute
from multiprocessing import Process
import os,sys,time
import pickle,redis
import django

sys.path.append('D:\code\joom_scrapy')
os.environ['DJANGO_SETTINGS_MODULE']='joom_scrapy.settings'
django.setup()
from fetch.models import ItemUrl

def run_scrapy():
    # execute(['scrapy', 'crawl', 'wish'])
    execute(['scrapy', 'crawl', 'joom'])

if __name__ =='__main__':
    client = redis.StrictRedis()

    jobs = ItemUrl.objects.filter(state=0)
    client.delete('joom')

    for job in jobs:
        client.lpush('joom', pickle.dumps(job))

    processes =[]
    for _ in range(5):
        process=Process(target=run_scrapy)
        process.start()
        time.sleep(0.5)
        processes.append(process)

    for process in processes:
        process.join()