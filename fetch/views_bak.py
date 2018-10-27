# -*- coding:UTF-8 -*-
from rest_framework.response import Response
from . import serializers, models
from tools.viewsets import CreateOnlyViewSet
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,TimeoutException,WebDriverException
from selenium import webdriver
from decimal import Decimal
import time,logging
from threading import Thread
from queue import Queue

# Create your views here.
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] "%(message)s"',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

match = {
            5: "fiveStars",
            4: "fourStars",
            3: "threeStars",
            2: "twoStars",
            1: "oneStars"
        }


class StartScrapeView(CreateOnlyViewSet):
    serializer_class = serializers.StartScrapeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['start']:
            self.web_to_scrape()
        return Response('爬取完毕')

    def web_to_scrape(self):
        urls = models.ItemUrl.objects.filter(state=0)

        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        tasks = Queue()
        threads = []

        for url_str in urls:
            tasks.put(url_str)

        for _ in range(1):
            thread=FetchThread(tasks,chrome_options)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()


class FetchThread(Thread):

    def __init__(self,queue,chrome_options):
        super().__init__()
        self.queue = queue
        self.chrome_options=chrome_options

    def run(self):
        driver = webdriver.Chrome(chrome_options=self.chrome_options)
        while True:
            if self.queue.empty():
                break
            url_str=self.queue.get()
            url = url_str.url_str
            # 控制台打印信息
            logger.info('start scrapy %s' % url)
            source_id = url.split('/')[-1]

            driver.get(url)
            time.sleep(1)
            lacator = (By.CSS_SELECTOR, 'div[property="description"]')

            # 等待描述信息出现，如果不出现记录为爬取异常
            try:
                WebDriverWait(driver, 60).until(EC.presence_of_element_located(lacator))
            except TimeoutException:
                url_str.state = 3
                url_str.save()
                continue

            # 取得记录实例，根据定位信息填充相应的字段
            instance = models.ItemLog()
            instance.goods_name = driver.title

            instance.msrp,instance.price = self.handle_price(driver)

            if len(driver.find_elements_by_css_selector('span[itemprop="itemListElement"]')) < 3:
                time.sleep(5)
            instance.introduce = driver.find_element_by_css_selector('div[property="description"]').text
            instance.default_img = driver.find_element_by_css_selector('img[property="image"]').get_attribute('src')
            instance.list_img = '|'.join([thumb.get_attribute('srcset').split(', ')[-1].split(' ')[0] for thumb in
                                          driver.find_elements_by_css_selector('div[class*="swipe"] img')])
            instance.cate = driver.find_element_by_css_selector('span[itemprop="itemListElement"]:last-child').text
            instance.source_id = source_id
            instance.url = url
            instance.create_time = int(time.time())
            try:
                instance.average_score = Decimal(
                    driver.find_element_by_css_selector('span[itemprop="ratingValue"]').text)
            except NoSuchElementException:
                pass
            for i in range(1, 6):
                try:
                    val = driver.find_element_by_css_selector('a[href*="reviewsType=%s"]' % match[i]).text
                    setattr(instance, 'score%s' % i, val.split('(')[1].split(')')[0].split('+')[0])
                except NoSuchElementException:
                    pass

            # 记录颜色和尺码信息
            colors = driver.find_elements_by_css_selector('span[class*="colorName"]')
            sizes = driver.find_elements_by_css_selector('div[class*="sizeWrapper"]')
            if sizes and not colors:
                self.iter_color(driver,colors,sizes,source_id,change=True)
            else:
                self.iter_color(driver,sizes,colors,source_id)


            # 保存爬取实例，并将状态修改为已爬取
            instance.save()
            url_str.state = 2
            url_str.save()
        driver.quit()

    def iter_color(self,driver,sizes,colors,source_id,change=False):
        for color in colors:
            try:
                color.find_element_by_xpath('./..').click()
            except WebDriverException:
                continue

            if sizes:
                for size in sizes:
                    try:
                        size.find_element_by_xpath('./..').click()
                    except WebDriverException:
                        continue
                    price,msrp=self.handle_price(driver)

                    models.ItemSkuLog.objects.create(color=size.text if change else color.text,msrp=msrp,size=color.text if change else size.text,source_id=source_id,price=price,create_time=int(time.time()))
            else:
                price, msrp = self.handle_price(driver)
                models.ItemSkuLog.objects.create(color=color.text, msrp=msrp, source_id=source_id,
                                                 price=price, create_time=int(time.time()))

    def handle_price(self,driver):
        prices = driver.find_element_by_css_selector('div[class*="prices"]').find_elements_by_tag_name('div')
        if len(prices) >= 3:
            msrp = Decimal(prices[0].text.split('$')[-1].split('\n')[0])
            price = Decimal(prices[1].text.split('$')[-1].split('\n')[0])
        else:
            price = Decimal(prices[0].text.split('$')[-1])
            msrp=Decimal(0.00)

        return price,msrp

