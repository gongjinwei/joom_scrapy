# -*- coding:UTF-8 -*-
from scrapy.cmdline import execute
from multiprocessing import Process


def run_scrapy():
    # execute(['scrapy', 'crawl', 'wish'])
    execute(['scrapy', 'crawl', 'joom'])


if __name__ =='__main__':

    processes =[]
    for _ in range(4):
        process=Process(target=run_scrapy)
        process.start()
        processes.append(process)

    for process in processes:
        process.join()