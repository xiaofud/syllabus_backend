# coding=utf-8
__author__ = 'smallfly'

# 一些错误常量
ERROR_NOT_FOUND = 1
ERROR_COMMIT_FAILED = 2


# 一些通用操作
def query_by_id(model, id_):
    """
    返回表中主键值为id_的记录
    :param model: 表的模型
    :param id_: 主键
    :return:    记录 或者 None
    """
    return model.query.filter_by(id=id_).first()

def commit_to_db(db, thing):
    db.session.add(thing)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(str(e))
        return False, ERROR_COMMIT_FAILED

def update_model_by_id(model, db, id, **kwargs):
    # 先找到对应的数据库记录
    thing = query_by_id(model, id)
    # 不存在该用户
    if thing is None:
        return False, ERROR_NOT_FOUND
    attrs = list()
    for attr in dir(thing):
        if not attr.startswith("__") and not attr.startswith("_"):
            attrs.append(attr)

    for key in kwargs:
        if key in attrs:
            if kwargs[key] is not None:
                setattr(thing, key, kwargs[key])

    # 保存修改
    return commit_to_db(db, thing)