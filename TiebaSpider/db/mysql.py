# -*- coding: utf-8 -*-
"""
mysql
~
关于数据库方面的操作
:copyright: (c) 2017 by comwrg.
:license: MIT, see LICENSE for more details.
"""

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session

from tables import Base


class mysql(object):
    def __init__(self, user, pwd, host, port, database):
        engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'
                       .format(user=user, password=pwd, host=host, port=port, database=database),
                               echo=False,
                               )
        self.session_factory = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)

    def session(self):
        return self.session_factory()

    def insert(self, o):
        session = self.session()
        try:
            session.add(o)
            session.commit()
        except:
            raise
        finally:
            session.close()

