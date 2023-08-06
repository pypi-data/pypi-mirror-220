import pymysql
from error import ClientError
from sql_db_base import SqlBase


class MysqlClass(SqlBase):
    """
    mysql工具类(no delete)---pymysql: 1.0.2 +

    tips: {'host','port','user','password','database'}
    """

    @property
    def db(self):
        """
        连接mysql

        :return: db
        """
        try:
            db = pymysql.connect(**self.settings)
        except Exception as e:
            raise ClientError('mysql client db error: ' + str(e.args))
        return db
