# -*- coding: utf-8 -*-
"""
config
~
有关yaml的操作
:copyright: (c) 2017 by comwrg.
:license: MIT, see LICENSE for more details.
"""

import yaml

def read(fp):
    y = yaml.load(fp)
    return y