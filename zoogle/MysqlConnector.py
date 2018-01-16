# -*- coding: utf-8 -*-
# author = 'BlackSesion'

import settings
from mysql import connector


class MysqlConnector(object):
    _db = None

    @staticmethod
    def connection():
        db = connector.connect(host=settings.DB_HOST, user=settings.DB_USER, passwd=settings.DB_PASSWD,
                               db=settings.DB_DBNAME)
        return db

    def get_connection(self):
        if self._db is None:
            self._db = self.connection()

        return self._db
