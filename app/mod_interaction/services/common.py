# coding=utf-8
__author__ = 'smallfly'

# 一些通用操作
def query_by_id(model, id_):
    """
    返回表中主键值为id_的记录
    :param model: 表的模型
    :param id_: 主键
    :return:    记录 或者 None
    """
    return model.query.filter_by(id=id_).first()