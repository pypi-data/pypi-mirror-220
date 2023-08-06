from dateutil.relativedelta import relativedelta
from error import TargetError, ParamsError
from datetime import datetime, timedelta
from typing import Union

# days_of_month_non_leap_year = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# days_of_month_leap_year = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def formatting(date_time: Union[str, datetime], original: Union[str, datetime], target: Union[str, datetime]):
    """
    对传入时间进行指定类型格式化

    :param date_time: 传入的时间，时间常见格式字符串、datetime对象
    :param original: 原始格式，时间常见格式字符串、datetime对象
    :param target: 目标格式，时间常见格式字符串、datetime对象
    :return: result
    """
    if isinstance(original, datetime) and isinstance(target, datetime):
        raise TargetError('original and target cannot be datetime')
    if isinstance(original, datetime) and isinstance(target, str):
        return datetime_to_str(date_time, target)
    if isinstance(original, str) and isinstance(target, datetime):
        return str_to_datetime(date_time, original)
    if isinstance(original, str) and isinstance(target, str):
        return str_to_str(date_time, original, target)
    raise TargetError('input target error')


def datetime_to_str(date_time: datetime, target: str):
    """
    格式化为字符串

    :return: result
    """
    return date_time.strftime(target)


def str_to_datetime(date_time: str, original: str):
    """
    格式化为datetime

    :return: result
    """
    return datetime.strptime(date_time, original)


def str_to_str(date_time: str, original: str, target: str):
    """
    格式化为字符串

    :return: result
    """
    dtime = datetime.strptime(date_time, original)
    return dtime.strftime(target)


def datetime_offset(date_time: datetime, year: int = 0, month: int = 0,
                    day: int = 0, hour: int = 0, minute: int = 0, second: int = 0):
    """
    计算传入时间偏移量

    :param date_time: 需要偏移的时间，datetime
    :param year: offset year
    :param month: offset month
    :param day: offset day
    :param hour: offset hour
    :param minute: offset minute
    :param second: offset second
    :return: result
    """
    if year:
        date_time = date_time + relativedelta(years=year)
    if month:
        date_time = date_time + relativedelta(months=month)
    return date_time + timedelta(days=day, hours=hour, minutes=minute, seconds=second)


def judge_leap_year(year):
    """
    判断是否为闰年
    """
    if year % 400 == 0 or year % 100 == 0 or year % 4 == 0:
        return True
    return False


def clac_datetime_differ(start: datetime, end: datetime, diff_type: str, only: bool = True):
    """
    计算两时间之差

    :param start: 需计算时间1
    :param end: 需计算时间2
    :param diff_type: 需计算类型
    :param only: 是否只计算传入量级，量级向上兼容，非量级计算不严格精准
    :return: result
    """
    # 参数判断
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise ParamsError('start or end is not datetime')
    # 允许传参集合
    diff_params = ('year', 'month', 'day', 'hour', 'minute', 'second')
    # 参数判断
    if diff_type not in diff_params:
        raise ParamsError(f'diff_type must in {str(diff_params)}')
    # 相等时间排异
    if start == end:
        return 0
    if start > end:
        start, end = end, start
    return globals()['clac_' + diff_type](start, end, only)


def clac_year(start, end, only):
    if only:
        return int(end.strftime('%Y')) - int(start.strftime('%Y'))
    return round(((end - start).days + 1) / 365, 2)


def clac_month(start, end, only):
    if only:
        return (int(end.strftime('%Y')) - int(start.strftime('%Y'))) * 12 \
               + (int(end.strftime('%m')) - int(start.strftime('%m'))) + 1
    return round(((end - start).days + 1) / 365 * 12, 2)


def clac_day(start, end, only):
    diff = end - start
    if only:
        return diff.days
    return round(diff.days + diff.seconds / 86400, 2)


def clac_hour(start, end, only):
    diff = end - start
    if only:
        return diff.days * 24 + int(diff.seconds / 3600)
    return round(diff.days * 24 + diff.seconds / 3600, 2)


def clac_minute(start, end, only):
    diff = end - start
    if only:
        return diff.days * 1440 + int(diff.seconds / 60)
    return round(diff.days * 1440 + diff.seconds / 60, 2)


def clac_second(start, end, only):
    diff = end - start
    return diff.days * 86400 + diff.seconds
