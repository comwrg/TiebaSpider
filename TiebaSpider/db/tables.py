# -*- coding: utf-8 -*-
"""
table
~
数据库表定义
:copyright: (c) 2017 by comwrg.
:license: MIT, see LICENSE for more details.
"""

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Thread(Base):
    __tablename__ = 'thread'
    mysql_charset = 'utf8mb4'

    id = Column(BIGINT, primary_key=True)
    title = Column(VARCHAR(100))
    author = Column(VARCHAR(30))
    reply_num = Column(INT())
    is_good = Column(BOOLEAN)

class Post(Base):
    __tablename__ = 'post'
    mysql_charset = 'utf8mb4'

    id = Column(BIGINT, primary_key=True)
    floor = Column(INT())
    author = Column(VARCHAR(30))
    content = Column(TEXT)
    time = Column(DATETIME)
    comment_num = Column(INT())
    thread_id = Column(ForeignKey('thread.id'))

class Comment(Base):
    __tablename__ = 'comment'
    mysql_charset = 'utf8mb4'

    id = Column(BIGINT(), primary_key=True)
    author = Column(VARCHAR(30))
    content = Column(TEXT)
    time = Column(DATETIME)
    post_id = Column(BIGINT())

