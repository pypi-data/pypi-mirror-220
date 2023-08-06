import xgcondb
import platform
from sql_db_base import SqlBase
from error import ClientError, InitDBError


class XGClass(SqlBase):
    """
    虚谷工具类(no delete)---包内自带此连接工具，限linux

    tips: {'host','port','user','password','database'}
    """
    def __init__(self, settings):
        super(XGClass, self).__init__(settings)
        if platform.system() == 'Windows':
            raise InitDBError('xu_gu db not init on windows')

    @property
    def db(self):
        """
        连接虚谷

        :return: db
        """
        try:
            db = xgcondb.connect(charset='utf8', **self.settings)
        except Exception as e:
            raise ClientError('xg client db error: ' + str(e.args))
        return db
