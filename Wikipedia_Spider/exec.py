#!/usr/bin/env python
# encoding: utf-8

'''
@author: whip1ash
@contact: security@whip1ash.cn
@software: pycharm 
@file: exec.py
@time: 2019/12/29 16:02
@desc:
'''

from scrapy import cmdline

cmdline.execute("scrapy crawl WikipediaSpider -o output.json".split())