import platform
import cx_Oracle
from error import ClientError
from sql_db_base import SqlBase


class OracleClass(SqlBase):
    """
    oracle工具类(no delete)---cx_Oracle: 8.3.0 +

    tips: {'host','port','user','password','database'}
    """

    def __init__(self, oci_path, settings):
        super(OracleClass, self).__init__(settings)
        if platform.system() == 'Windows':
            cx_Oracle.init_oracle_client(oci_path)

    @property
    def db(self):
        """
        连接mysql

        :return: db
        """
        try:
            db = cx_Oracle.connect(
                *(self.settings.user,
                  self.settings.password,
                  f'{self.settings.host}:{self.settings.port}/{self.settings.database}'))
        except Exception as e:
            raise ClientError('oracle client db error: ' + str(e))
        return db
