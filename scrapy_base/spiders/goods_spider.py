import json
from sys import flags
from typing import ItemsView
import scrapy
import re
from pyquery import PyQuery as pq
from lxml import etree
import urllib
from scrapy_base.items import PipelineBasedSavedItem
from scrapy_splash import SplashRequest


class GoodsSpider(scrapy.Spider):
    name = "goods"
    data = []

    def start_requests(self):
        url_template_num = 2

        def get_url(url_template_num):
            return f'https://fuli.colipu.com/fulicategory-20010-{url_template_num}-1-a-a.html'

        urls = []
        for i in range(0, 5):
            urls.append(get_url(url_template_num + i))
        for url in urls:
            yield SplashRequest(url=url, callback=self.parsePage)

    def parsePage(self, response):
        jq = pq(response.text)
        urls = []
        baseurl = 'https://fuli.colipu.com'
        for i in jq('#productlist > ul:nth-child(1) > li > div:nth-child(1) > a:nth-child(1)'):
            urls.append(baseurl+i.attrib['href'])
        for url in urls:
            yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
        jq = pq(response.text)
        item = PipelineBasedSavedItem()
        item['id'] = re.findall(r"(?<=：).{5,}?(?=\D)", response.xpath(
            '//*[@id="details"]/div[1]/div[1]/div[2]/text()').get())[0]
        item['name'] = response.xpath(
            '/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/b/text()').get()
        item['breadcrumbs'] = [
            response.xpath(
                '//*[@id="main-body"]/div[1]/ul/li[2]/a/text()').get(),
            response.xpath(
                '//*[@id="main-body"]/div[1]/ul/li[3]/a/text()').get(),
            response.xpath(
                '//*[@id="main-body"]/div[1]/ul/li[4]/a/text()').get(),
        ]
        item['price'] = jq(
            '.product-price > div:nth-child(2) > span:nth-child(1)').text()
        item['price2'] = response.xpath(
            '//*[@id="details"]/div[1]/div[2]/div[2]/div/b/text()').get() if response.xpath(
            '//*[@id="details"]/div[1]/div[2]/div[2]/div/b/text()').get() else ""
        item['parameters'] = jq(
            '#details > div.container.product-content > div.product-right > div > div.product-body-default.attrText > div.product-body-param > ul').text()
        item['categories'] = jq(
            '#details > div.container.product-content > div.product-left > dl > dd').text()
        item['exhibitions'] = []
        for i in jq(
                'html body div#main-body.main div#details div.container div.product-imgnumber div.product-img div.product-imgsmall div#ul.product-imgsmall-img ul img'):
            item['exhibitions'].append(i.attrib['src'])
        item['details'] = []
        jq(
            '#details > div.container.product-content > div.product-right > div > div.product-body-default.attrText > div.product-body-main > div > img').each(lambda i, e: item['details'].append(e.attrib['src']))

        yield item
