# -*- coding: utf-8 -*-
"""
mysql
~
关于数据库方面的操作
:copyright: (c) 2017 by comwrg.
:license: MIT, see LICENSE for more details.
"""

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker, scoped_session

from tables import Base


class mysql(object):
    def __init__(self, user, pwd, host, port, database):
        self.engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'
                       .format(user=user, password=pwd, host=host, port=port, database=''),
                               echo=False,
                               )
        self.session_factory = sessionmaker(bind=self.engine)

        self.execute('SET NAMES utf8mb4')
        self.create_database(database)
        self.use_database(database)
        Base.metadata.create_all(self.engine)

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

    def execute(self, s):
        session = self.session()
        try:
            session.execute(s)
        except:
            raise
        finally:
            session.close()

    def create_database(self, database):
        conn = self.engine.connect()
        try:
            conn.execute('CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4'.format(database=database))
        except:
            raise
        finally:
            conn.close()

    def use_database(self, database):
        conn = self.engine.connect()
        try:
            conn.execute('USE {database}'.format(database=database))
        except:
            raise
        finally:
            conn.close()
