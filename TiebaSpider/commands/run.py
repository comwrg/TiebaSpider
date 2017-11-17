# -*- coding: utf-8 -*-
"""
run
~
重写 Scrapy Command 模块
:copyright: (c) 2017 by comwrg.
:license: MIT, see LICENSE for more details.
"""

import scrapy.commands.crawl
from scrapy.commands import ScrapyCommand


class Command(scrapy.commands.crawl.Command):
    def syntax(self):
        return '<tieba>'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        # default options
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")

        ##################

    def run(self, args, opt):
        self.settings['tieba'] = args[0]

        self.crawler_process.crawl('tieba', **opt.spargs)
        self.crawler_process.start()



