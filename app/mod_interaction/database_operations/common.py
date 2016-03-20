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

def add_to_db(db, thing):
    try:
        db.session.add(thing)
        db.session.commit()
        return True
    except Exception as e:
        print(str(e))
        db.session.rollback()
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
    return add_to_db(db, thing)

def get_last_inserted_id(model):
    # with_entities(model.field, xxx)    # 仅仅取指定的字段
    return model.query.with_entities(model.id).order_by(model.id.desc()).first().id

def new_record(db, model, **kwargs):
    thing = model(**kwargs)
    result = add_to_db(db, thing)
    if result == True:

        return get_last_inserted_id(model)
    else:
        return False

def delete_from_db(db, model, id):
    thing = query_by_id(model, id)
    # print(thing)
    if thing is None:
        return False, ERROR_NOT_FOUND
    try:
        db.session.delete(thing)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        db.session.rollback()
        return False, ERROR_COMMIT_FAILED