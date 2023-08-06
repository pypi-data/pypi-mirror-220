from collections import Counter
from functools import wraps


class Dict(dict):
    """
    重写字典对象，添加__setitem__，__getitem__魔术方法
    """
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    def __getstate__(self):
        """
        添加可序列化魔术方法，否则协程迟报错（协程任务参数必须可序列化）
        """
        ...


def dict_to_object(data):
    """
    字典转化为Dict对象
    ----------
    data: 无特定类型，dict进行分解，其他赋为对应键的值
    ----------
    Dict对象形字典
    """
    if not isinstance(data, dict):
        return data
    inst = Dict()
    for k, v in data.items():
        inst[k] = dict_to_object(v)
    return inst


def judge_params(template: list, params: dict):
    """
    :param template: 参数模板，连接类内部定义
    :param params: 传入参数
    :return: 对比结果
    """
    if dict(Counter(template)) == dict(Counter(params.keys())):
        return True
    return False


def retry_result(function):
    """
    对增查改方法进行运行结果订正

    :return: result
    """
    @wraps(function)
    def func(*args, **kwargs):
        try:
            res = function(*args, **kwargs)
            if 'search' in function.__name__:
                return res
            return True
        except Exception as e:
            print('%s-%s: %s' % (function.__qualname__, function.__name__, str(e)))
            return False
    return func
