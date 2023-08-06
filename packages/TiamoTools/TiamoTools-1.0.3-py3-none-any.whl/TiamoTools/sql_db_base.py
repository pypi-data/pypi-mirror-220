from error import ParamsError
from common import dict_to_object, judge_params, retry_result


class CursorInit:
    @classmethod
    def execute(cls, *args, **kwargs):
        ...

    @classmethod
    def executemany(cls, *args, **kwargs):
        ...

    @classmethod
    def fetchall(cls, *args, **kwargs):
        ...


class DbInit:
    @classmethod
    def cursor(cls):
        return CursorInit()

    @classmethod
    def close(cls):
        ...

    @classmethod
    def commit(cls):
        ...


class SqlClientBase:
    """
    sql连接类

    tips: {'host','port','user','password','database'}
    """
    __params_template = ['host', 'port', 'user', 'password', 'database']

    def __init__(self, settings: dict):
        """
        :param settings: 数据库信息
        """
        if not judge_params(self.__params_template, settings):
            raise ParamsError('params error')
        self.settings = dict_to_object(settings)

    @property
    def db(self):
        return DbInit()

    def release(self):
        """
        释放数据量连接
        """
        return self.db.close()


class SqlBase(SqlClientBase):
    """
    sql工具类(no delete)
    """

    @retry_result
    def search(self, sql: str):
        """
        mysql查询

        :param sql: sql语句
        :return: data
        """
        cur = self.db.cursor()
        cur.execute(sql)
        return cur.fetchall()

    @retry_result
    def insert(self, sql: str):
        """
        mysql单条数据插入

        :param sql: sql语句
        :return: data
        """
        cur = self.db.cursor()
        cur.execute(sql)
        self.db.commit()
        return True

    @retry_result
    def insert_many(self, sql: str, data: list):
        """
        mysql多条数据插入

        :param sql: sql语句
        :param data: 数据集合，List[Tuple]
        :return: data
        """
        cur = self.db.cursor()
        cur.executemany(sql, data)
        self.db.commit()
        return True

    @retry_result
    def update(self, sql: str):
        """
        mysql单条数据更新

        :param sql: sql语句
        :return: data
        """
        cur = self.db.cursor()
        cur.execute(sql)
        self.db.commit()
        return True

    @retry_result
    def update_many(self, sql: str, data: list):
        """
        多约束多条数据更新

        :param sql: sql语句
        :param data: 数据集合,包含约束数据、更新数据，List[Tuple]
        :return: data
        """
        cur = self.db.cursor()
        cur.executemany(sql, data)
        self.db.commit()
        return True
