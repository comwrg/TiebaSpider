# -*- coding: utf-8 -*-
"""
utils
~
页面转换方面操作
:copyright: (c) 2017 by comwrg.
:license: MIT, see LICENSE for more details.
"""

from bs4 import BeautifulSoup
import re

def parse_content(content, is_post):
    if not content or not content.strip():
        return None
    content = content.replace('\r', '\n')
    s = BeautifulSoup(content, 'lxml')
    if is_post:
        s = s.div

    l = list(s.children)
    for i in range(len(l)):
        parse_func = (is_str, is_br, other_case)
        for func in parse_func:
            try:
                ret = func(l[i])
            except:
                continue
            if ret is not False:
                l[i] = ret
                break
    return strip_blank(''.join(l))

def strip_blank(s): #按个人喜好去掉空白字符
    s = re.sub(r'\n[ \t]+\n', '\n', s)
    s = re.sub(r'  +', ' ', s) #去掉多余的空格
    s = re.sub(r'\n\n\n+', '\n\n', s) #去掉过多的连续换行
    return s.strip()

def is_str(s):
    if s.name:
        return False
    #NavigableString类型需要手动转换下
    return unicode(s)

def is_br(s):
    if s.name == 'br':
        return '\n'
    return False

#bs带的get_text功能，很好很强大
#粗体红字之类的都一句话搞定了
def other_case(s):
    return s.get_text()