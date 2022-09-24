# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from pyquery import PyQuery as pq
import time
import random
from urllib.parse import quote
import csv


def deep_traversal(data):
    if isinstance(data, dict):
        for k in data:
            if isinstance(data[k], str):
                data[k] = data[k].strip()
            else:
                yield from deep_traversal(data[k])
    elif isinstance(data, list):
        for k in range(len(data)):
            if isinstance(data[k], str):
                data[k] = data[k].strip()
            else:
                yield from deep_traversal(data[k])


class ScrapyBasePipeline:
    def process_item(self, item, spider):
        return item


class PipelineBasedSavedPipeline:
    def __init__(self):
        self.file = None
        self.line = {"name": 0, "id": 0, "breadcrumbs": 0,
                     "price": 0, "price2": 0, "parameters": 0, "categories": 0, "exhibitions": 0, "date": 0, "sales": 0, 'details': 0}
    # 开始爬虫时执行, 打开文件

    def open_spider(self, spider):
        self.file = open('data.csv', 'w', encoding='utf-8', newline='')
        writer = csv.writer(self.file, dialect='excel')
        writer.writerow(self.line.keys())

    # 结束爬虫时执行, 关闭文件

    def close_spider(self, spider):
        self.file.close()

    # 对提交的item处理(写入操作)
    def process_item(self, item, spider):
        self.line['id'] = item['id']
        self.line['name'] = item['name']
        self.line['breadcrumbs'] = item['breadcrumbs']
        self.line['price'] = item['price']
        price2 = item['price2']
        if price2:
            price2 = price2[price2.index('¥'):]
            price2 = price2.replace('\r\n', ' ')
        self.line['price2'] = price2
        parameters = item['parameters']
        if parameters:
            list = parameters.split('\n')
            parameters = {}
            for value in list:
                value = value.split('：')
                if len(value) == 2:
                    parameters[value[0]] = value[1]
        else:
            parameters = {}
        self.line['parameters'] = parameters
        categories = item['categories']
        if categories:
            list = categories.split(' ')
            categories = []
            for value in list:
                if value == '':
                    break
                categories.append(value)
        else:
            categories = []
        self.line['categories'] = categories
        self.line['exhibitions'] = item['exhibitions']
        self.line['details'] = item['details']

        def random_date():
            a1 = (2010, 1, 1, 0, 0, 0, 0, 0, 0)
            # 设置开始日期时间元组
            # 设置结束日期时间元组
            a2 = (2022, 8, 31, 23, 59, 59, 0, 0, 0)

            start = time.mktime(a1)  # 生成开始时间戳
            end = time.mktime(a2)  # 生成结束时间戳

            # 随机生成10个日期字符串
            t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
            date_touple = time.localtime(t)  # 将时间戳生成时间元组
            # 将时间元组转成格式化字符串（1976-05-21）
            date = time.strftime("%Y-%m-%d", date_touple)
            return date

        self.line['date'] = random_date()
        self.line['sales'] = random.randint(1, 1000)

        for i in deep_traversal(self.line):
            pass
        for key in self.line:
            self.line[key] = json.dumps(self.line[key], ensure_ascii=False)
        writer = csv.writer(self.file, dialect='excel')
        writer.writerow(self.line.values())
        return self.line
