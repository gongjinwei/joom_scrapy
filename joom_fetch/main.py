# -*- coding:UTF-8 -*-
from scrapy.cmdline import execute

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import os

dirname =os.path.abspath(os.path.dirname(__file__))
if os.getcwd()!=dirname:
    os.chdir(os.path.dirname(__file__))

process = CrawlerProcess(get_project_settings())

for _ in range(4):
    # process.crawl('wish')
    process.crawl('wish_api')
    # process.crawl('joom')

process.start()

# execute(['scrapy', 'crawl', 'wish'])
# execute(['scrapy', 'crawl', 'joom'])