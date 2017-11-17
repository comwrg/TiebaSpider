# -*- coding: utf-8 -*-
"""
spider
~
提取html中的信息
:copyright: (c) 2017 by comwrg.
:license: MIT, see LICENSE for more details.
"""

import scrapy
import json
from sqlalchemy.exc import IntegrityError

from TiebaSpider.items import *
from TiebaSpider.utils import parse


class TiebaSpider(scrapy.Spider):
    name = 'tieba'

    def parse(self, response):
        for post in response.xpath('//li[contains(@class, "j_thread_list")]'):
            data = json.loads(post.xpath('@data-field').extract_first())
            item = ThreadItem()
            item['id'] = data['id']
            item['author'] = data['author_name']
            item['reply_num'] = data['reply_num']
            item['is_good'] = data['is_good']
            if not item['is_good']:
                item['is_good'] = False
            item['title'] = post.xpath('.//div[contains(@class, "threadlist_title")]/a/text()').extract_first()
            yield item
            meta = {
                'thread_id': data['id'],
                'page'     : 1,
            }
            url = 'http://tieba.baidu.com/p/{0}'.format(data['id'])
            yield scrapy.Request(url, callback=self.parse_post, meta=meta)
        next_page = response.xpath('//a[@class="next pagination-item "]/@href')
        if next_page:
            yield self.make_requests_from_url('http:{0}'.format(next_page.extract_first()))

    def parse_post(self, response):
        meta = response.meta
        for floor in response.xpath("//div[contains(@class, 'l_post')]"):
            data = json.loads(floor.xpath("@data-field").extract_first())
            item = PostItem()
            item['id'] = data['content']['post_id']
            item['author'] = data['author']['user_name']
            item['comment_num'] = data['content']['comment_num']
            item['thread_id'] = meta['thread_id']
            item['floor'] = data['content']['post_no']
            if 'date' in data['content']:
                item['time'] = data['content']['date']
            else:
                item['time'] = floor.xpath(".//span[@class='tail-info']") \
                    .re_first(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}')
            content = floor.xpath(".//div[contains(@class, 'j_d_post_content')]").extract_first()
            item['content'] = parse.parse_content(content, True)
            yield item
        next_page = response.xpath(u".//ul[@class='l_posts_num']//a[text()='下一页']/@href")
        if next_page:
            meta['page'] += 1
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, callback=self.parse_post, meta=meta)



