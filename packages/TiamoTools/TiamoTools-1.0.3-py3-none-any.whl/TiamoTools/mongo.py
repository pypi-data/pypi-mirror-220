import pymongo
from typing import List
from pymongo import MongoClient
from error import ParamsError, ClientError
from common import dict_to_object, judge_params, retry_result


class MongoClass:
    """
    mongodb工具类(no delete)---pymongo: 3.8.0 +

    tips: {'host':''/List,'port','user','password','db','is_group':True/False}
    """
    __params_template = ['host', 'port', 'user', 'password', 'db', 'is_group']

    def __init__(self, settings: dict):
        """
        :param settings: 数据库信息
        """
        if not judge_params(self.__params_template, settings):
            raise ParamsError('params error')
        self.settings = dict_to_object(settings)

    @property
    def client(self):
        """
        连接mongodb

        :return: client
        """
        try:
            if self.settings.is_group:
                client = MongoClient(self.settings.host)
            else:
                client = MongoClient(host=self.settings.host, port=self.settings.port)
            client.admin.authenticate(self.settings.user, self.settings.password)
        except Exception as e:
            raise ClientError('mongo client error: ' + str(e.args))
        return client

    @property
    def db(self):
        """
        连接数据库

        :return: db连接
        """
        try:
            client = self.client
            return client[self.settings.db]
        except Exception as e:
            raise ClientError('client db error: ' + str(e.args))

    def release(self):
        """
        释放mongo连接
        """
        return self.client.close()

    @retry_result
    def search(self, table: str, query_dict: dict):
        """
        :param table: 目标数据表
        :param query_dict: query
        :return: result
        """
        db = self.db[table]
        return db.find(query_dict)

    @retry_result
    def insert(self, table: str, query_dict: dict):
        """
        :param table: 目标数据表
        :param query_dict: query
        :return: result
        """
        db = self.db[table]
        return db.insert_one(query_dict)

    @retry_result
    def insert_many(self, table: str, query_dict: List[dict]):
        """
        :param table: 目标数据表
        :param query_dict: query
        :return: result
        """
        db = self.db[table]
        return db.insert_many(query_dict)

    @retry_result
    def update(self, table: str, filter_query: dict, set_query: dict):
        """
        更新操作，查询到约束条件则更新，否则执行插入操作

        tips: db.test.update({'_id': 'id'}, {'$set': {'b': 'b'}}, true)

        :param table: 目标数据表
        :param filter_query: 查询query
        :param set_query: 数据query
        :return: result
        """
        db = self.db[table]
        return db.update_one(filter_query, set_query, upsert=True)

    @retry_result
    def update_many(self, table: str, bulk_query: List[List[dict]]):
        """
        多约束多数据更新操作，查询到约束条件则更新，否则执行插入操作

        tips1: [[{'sex': '男'}, {'$set': {'is_qualified': False}}],...]

        tips2: db.bulk_write([
          pymongo.UpdateMany({'sex': '男'}, {'$set': {'is_qualified': False}}),

          pymongo.UpdateMany({'sex': '女'}, {'$set': {'is_qualified': True}})])

        :param table: 目标数据表
        :param bulk_query: 批量操作query集合
        :return: result
        """
        db = self.db[table]
        bulk_query = [pymongo.UpdateMany(query[0], query[1], upsert=True) for query in bulk_query]
        return db.bulk_write(bulk_query)

    # def delete(self, table: str, query_dict: dict):
    #     """
    #     :param table: 目标数据表
    #     :param query_dict: query
    #     :return: result
    #     """
    #     db = self.db[table]
    #     return db.delete_one(query_dict)
    #
    # def delete_many(self, table: str, query_dict: dict):
    #     """
    #     :param table: 目标数据表
    #     :param query_dict: query
    #     :return: result
    #     """
    #     db = self.db[table]
    #     return db.delete_many(query_dict)
