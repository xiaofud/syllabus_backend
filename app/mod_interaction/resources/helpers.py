# coding=utf-8
__author__ = 'smallfly'

from datetime import datetime

def clean_arguments(args, accepted):
    """
    清除不在 accepted 列表内的 键值对
    :param args: 原来的字典
    :param accepted: 允许的字段
    :return: None
    """
    for arg in args:
        if arg not in accepted:
            assert isinstance(args, dict)
            args.pop(arg)


def timestamp_to_string(timestamp, format="%Y-%m-%d %H:%M:%S"):
    """
    将timestamp转换成时间
    :param timestamp:
    :return:
    """
    time_string = datetime.fromtimestamp(int(timestamp))
    time_string = time_string.strftime(format)
    return time_string