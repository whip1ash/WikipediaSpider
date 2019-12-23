#!/usr/bin/env python
# encoding: utf-8

'''
@author: whip1ash
@contact: security@whip1ash.cn
@software: pycharm 
@file: wikipedia_spider.py
@time: 2019/12/22 07:59
@desc:
'''


from urllib.parse import unquote
import scrapy

class WikipediaSpider(scrapy.Spider):
    name = "WikipediaSpider"
    entities = list()
    start_urls = [
        'https://en.wikipedia.org/wiki/Voltage'
    ]

    def parse(self, response):
        next_entities = list()

        entity = response.css('h1.firstHeading::text').get()
        self.entities.append(entity)

        # todo: 找到toc，然后正则匹配mw-parser-output到toc的p标签，解析其中的文本。
        desc = ''

        link_entities = response.xpath('//*[@id="mw-content-text"]/div/div[@role="navigation"]/following-sibling::div/ul/li/a/@href').getall()

        # 另外一种情况
        if not link_entities:
            link_entities = response.xpath(
                '//*[@id="mw-content-text"]/div/div[@role="navigation"]/following-sibling::ul[1]/li/a/@href').getall()

        # process entitles
        for i in link_entities:
            entitity_name = unquote(i.split('/')[-1],'utf-8')
            next_entities.append(entitity_name)

        if link_entities:
            yield {
                'entity': entity,
                'desc': desc,
                'nextEntity': ','.join(next_entities),
                'referer': response.request.headers.get('referer')
            }

            for link_entity in link_entities:
                entity = unquote(link_entity.split('/')[-1],'utf-8')

                print("entity name is " + entity)

                print(self.entities)
                if entity not in self.entities:
                    next_page = response.urljoin(link_entity)
                    yield scrapy.Request(next_page, callback=self.parse)


