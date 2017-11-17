# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting See:
# http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from urllib import quote

from sqlalchemy.exc import IntegrityError

from TiebaSpider.db.mysql import mysql
from TiebaSpider.db.tables import *
from TiebaSpider.utils import config
from TiebaSpider.utils.wrapper import ignore_exception


class TiebaspiderPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self, settings):
        self.settings = settings
        y = config.read(open('TiebaSpider/config.yaml'))
        db = y['db']
        self.mysql = mysql(db['user'], db['password'], db['host'], db['port'], db['database'])
        # log.msg('setting={0}'.format(settings))

    def open_spider(self, spider):
        spider.start_urls = [
            'http://tieba.baidu.com/f?kw={0}&pn={1}'.format(quote(self.settings["tieba"]), 1),
        ]

    @ignore_exception(IntegrityError)
    def process_item(self, item, spider):
        # log.msg('item={0}'.format(item))
        if item.name is 'thread':
            thread = Thread(
                id        = item['id'       ],
                title     = item['title'    ],
                author    = item['author'   ],
                reply_num = item['reply_num'],
                is_good   = item['is_good'  ],
            )
            self.mysql.insert(thread)
        elif item.name is 'post':
            post = Post(
                id=item['id'],
                floor=item['floor'],
                author=item['author'],
                content=item['content'],
                time=item['time'],
                comment_num=item['comment_num'],
                thread_id=item['thread_id'],
            )
            self.mysql.insert(post)
        return item
