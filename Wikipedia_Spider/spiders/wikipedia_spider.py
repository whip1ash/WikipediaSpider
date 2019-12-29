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
from scrapy.http import Request

class WikipediaSpider(scrapy.Spider):
    name = "WikipediaSpider"
    start_urls = [
        'https://en.wikipedia.org/wiki/Category:Electronics'
    ]

    def parse(self, response):

        # parse current entity name
        current_url = response.request.url
        entity_name = current_url.split(':')[-1]

        # parse referer entity name
        referer_url = response.request.headers.get('referer')
        if referer_url is None:
            # origin entity
            referer = "Electronics"
        else:
            referer_url = str(referer_url,encoding='utf-8')
            referer = referer_url.split(':')[-1]

        # get next entities
        next_entities = list()
        entities_href =  response.xpath('//*[@id="mw-subcategories"]/div/div/div/ul/li/div/div/a/@href').getall()
        for entity_href in entities_href:
            entity = entity_href.split(':')[-1]
            next_entities.append(entity)

        # get desc
        current_desc_hrefs = response.xpath('//*[@id="mw-pages"]/div/div/div[1]/ul/li/a/@href').getall()

        current_desc_href = ''
        hasDesc = False
        if current_desc_hrefs:
            for i in current_desc_hrefs:
                if i == "/wiki/" + entity_name:
                    current_desc_href = i
                    break

            if current_desc_href == '':
                desc = ''
            # 存在该实体的定义页面，发起请求
            else:
                hasDesc = True
                req_url = response.urljoin(current_desc_href)
                result = {}
                result['entity'] = entity_name
                result['parentNode'] = referer
                result['sonNode'] = next_entities
                result['currentUrl'] = current_url
                yield Request(url=req_url,callback=self.extrac_desc,meta={'res':result})

        # result is empty
        else:
            desc = ''

        # save result if desc is empty
        if not hasDesc:
            yield {
                "entity": entity_name,
                "desc" : desc,
                "parentNode" : referer,
                "sonNode" : next_entities,
                "currentUrl": current_url
            }

        for next in entities_href:
            print("next entity name is " + next)
            next_page = response.urljoin(next)
            yield scrapy.Request(next_page, callback=self.parse)

    def extrac_desc(self,response):
        result = response.meta['res']
        data = response.selector.xpath('//*[@id="mw-content-text"]/div/p[1]')
        desc = data.xpath('string(.)').extract()[0]
        result['desc'] = desc

        yield result

