# -*- coding:UTF-8 -*-
from scrapy.cmdline import execute

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import os

os.chdir(os.path.dirname(__file__))

process = CrawlerProcess(get_project_settings())

for _ in range(4):
    process.crawl('joom')

process.start()

# execute(['scrapy', 'crawl', 'wish'])
# execute(['scrapy', 'crawl', 'joom'])