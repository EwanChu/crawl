# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class CfSpider(CrawlSpider):
    name = 'cf'
    allowed_domains = ['circ.gov.cn']
    start_urls = ['http://bxjg.circ.gov.cn/web/site0/tab5240/module14430/page1.htm']

    # 定义提取url规则
    rules = (
        # LinkExtractor 链接提取器，提取url
        # callback 提取到的url的response交由那个函数处理
        # follow 表示URL对应的响应是否重新经过rules提取url地址
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/info\d+\.htm'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/module14430/page\d+\.htm'), follow=True),
    )
    # parse函数有特殊含义，所以不能自己定义

    def parse_item(self, response):
        item = {}
        item["title"] = re.findall("<!--TitleStart-->(.*?)<!--TitleEnd-->", response.body.decode())[0]
        item["publish_date"] = re.findall("发布时间：(20\d{2}-\d{2}-\d{2})", response.body.decode())[0]
        item["concent"] = response.xpath("//tr/td/span[@id='zoom']/p/text()").extract()
        print(item)
        return item
