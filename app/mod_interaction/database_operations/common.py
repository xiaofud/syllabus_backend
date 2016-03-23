# coding=utf-8
__author__ = 'smallfly'

# http://flask-sqlalchemy.pocoo.org/2.1/queries/#querying-records

# 一些错误常量
ERROR_NOT_FOUND = 1
ERROR_COMMIT_FAILED = 2
ERROR_USER_ID_CONFLICT = 3  # 要删除的资源的发布者和执行删除的人不对

# query 常量
QUERY_SORT_TYPE_ASC = 1 # 升序排列
QUERY_SORT_TYPE_DESC = 2    # 降序排列
QUERY_ORDER_BY_DEFAULT = "id"   # 默认按照id排序
QUERY_RESULT_COUNT_DEFAULT = 10 # 默认返回10条数据

QUERY_ATTR_SORT_TYPE = "sort_type"
QUERY_ATTR_COUNT = "count"
QUERY_ATTR_ORDER_BY = "order_by"
QUERY_ATTR_FILTER_FIELD = "field"
QUERY_ATTR_FILTER_VALUE = "value"

from app.mod_interaction.models import User

def try_to_int(the_str):
    try:
        return int(the_str)
    except ValueError as e:
        return False

# 一些通用操作
def query_single_by_id(model, id_):
    """
    返回表中主键值为id_的记录
    :param model: 表的模型
    :param id_: 主键
    :return:    记录 或者 None
    """
    # return model.query.filter_by(id=id_).first()
    # 参考文档
    return model.query.get(id_)



def query_multiple(model, **kwargs):
    # 因为传入的参数里面可能有的是None
    sorting = kwargs.pop(QUERY_ATTR_SORT_TYPE) or QUERY_SORT_TYPE_DESC  # 降序
    count = kwargs.pop(QUERY_ATTR_COUNT) or QUERY_RESULT_COUNT_DEFAULT   # 返回的数量
    order_by = kwargs.pop(QUERY_ATTR_ORDER_BY) or  QUERY_ORDER_BY_DEFAULT   # 按照什么排序

    if count <= 0 :
        count = QUERY_RESULT_COUNT_DEFAULT

    if not hasattr(model, order_by):
        return False


    if sorting == QUERY_SORT_TYPE_DESC:
        return model.query.order_by(getattr(model, order_by).desc()).limit(count).all()
    else:
        return model.query.order_by(getattr(model, order_by).asc()).limit(count).all()

def query_one_to_many(model, **kwargs):
    # 因为传入的参数里面可能有的是None
    sorting = kwargs.pop(QUERY_ATTR_SORT_TYPE) or QUERY_SORT_TYPE_DESC  # 降序
    count = kwargs.pop(QUERY_ATTR_COUNT) or QUERY_RESULT_COUNT_DEFAULT   # 返回的数量
    order_by = kwargs.pop(QUERY_ATTR_ORDER_BY) or  QUERY_ORDER_BY_DEFAULT   # 按照什么排序

    filed = kwargs.pop(QUERY_ATTR_FILTER_FIELD) or None
    value = kwargs.pop(QUERY_ATTR_FILTER_VALUE) or None

    # 如果可以转换成数字就转换为数字
    tmp = try_to_int(value)
    if tmp != False:
        value = tmp

    if filed is None:
        return False

    if not hasattr(model, filed) or not hasattr(model, order_by):
        # print("model has not ", filed)
        return False

    # print(model.__tablename__, " has ", filed)

    if sorting == QUERY_SORT_TYPE_DESC:
        return model.query.filter(getattr(model, filed) == value).order_by(getattr(model, order_by).desc()).limit(count).all()
    else:
        return model.query.filter(getattr(model, filed) == value).order_by(getattr(model, order_by).asc()).limit(count).all()


# def query(model, **kwargs):
#     if "id" in kwargs:
#         # 查找单个数据
#         return query_single_by_id(model, kwargs["id"])
#     if "count" in kwargs:
#         # 查找多个
#         return model.query.order_by(model.id.desc()).limit(int(kwargs["count"])).all()

def fetch_all(model):
    return model.query.all()

def add_to_db(db, thing):
    try:
        db.session.add(thing)
        db.session.commit()
        return True
    except Exception as e:
        print(str(e))
        db.session.rollback()
        return False, ERROR_COMMIT_FAILED

def update_model_by_id(model, db, id, uid, **kwargs):
    # 先找到对应的数据库记录
    thing = query_single_by_id(model, id)
    # 不存在该用户
    if thing is None:
        return False, ERROR_NOT_FOUND

    # 有可能寻找的用户数据, 所以这里需要判别一下
    if hasattr(thing, "uid"):
        if thing.uid != uid:
            return False, ERROR_USER_ID_CONFLICT
    else:
        if id != uid:
            return False, ERROR_USER_ID_CONFLICT

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

def delete_from_db(db, model, id, uid):
    thing = query_single_by_id(model, id)
    # print(thing)
    if thing is None:
        return False, ERROR_NOT_FOUND

    # 检查有没有权限删除
    if thing.uid != uid:
        return False, ERROR_USER_ID_CONFLICT
    try:
        db.session.delete(thing)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        db.session.rollback()
        return False, ERROR_COMMIT_FAILED

def check_token(args):
    uid = args.get("uid")
    token = args.get("token")
    # print(uid, token)
    if uid is None or token is None:
        return False
    if uid is not None and token is not None:
        user = query_single_by_id(User, uid)
        if user is None:
            return False
        print("token for {} is {}".format(user.account, user.token))
        # print("real token {}, input token {}".format(user.token, token))
        if user.token == token:
            print("token is right")
            return True
    return False