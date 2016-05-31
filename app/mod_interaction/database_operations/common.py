# coding=utf-8
__author__ = 'smallfly'

# http://flask-sqlalchemy.pocoo.org/2.1/queries/#querying-records

from app.mod_interaction.models import User, VISIBILITY_VISIBLE, VISIBILITY_INVISIBLE, Comment
from app.mod_interaction.database_operations.comment_operation import new_unread
from config import config

# 一些错误常量
ERROR_NOT_FOUND = 1
ERROR_COMMIT_FAILED = 2
ERROR_USER_ID_CONFLICT = 3  # 要删除的资源的发布者和执行删除的人不对

# query 常量
QUERY_SORT_TYPE_ASC = 1 # 升序排列
QUERY_SORT_TYPE_DESC = 2    # 降序排列
QUERY_ORDER_BY_DEFAULT = "id"   # 默认按照id排序
QUERY_RESULT_COUNT_DEFAULT = 10 # 默认返回10条数据
# 注意默认不能是1, 因为offset就是直接针对第一个记录的偏移量
QUERY_BEFORE_ID_DEFAULT = 9999999999    # 获取最新的数据的意思

QUERY_ATTR_SORT_TYPE = "sort_type"
QUERY_ATTR_COUNT = "count"
QUERY_ATTR_ORDER_BY = "order_by"
QUERY_ATTR_FILTER_FIELD = "field"
QUERY_ATTR_FILTER_VALUE = "value"
QUERY_ATTR_BEFORE_ID = "before_id"  # 查找 id < after_id 的



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
    if hasattr(model, "visibility"):
        return model.query.filter_by(id=id_).filter_by(visibility=VISIBILITY_VISIBLE).first()
    else:
        return model.query.filter_by(id=id_).first()

    # 参考文档
    # return model.query.get(id_)

def query_single_by_filed(model, field, value):
    if not hasattr(model, field):
        return None
    kwargs = {
        field: value
    }
    if hasattr(model, "visibility"):
        return model.query.filter_by(**kwargs).filter_by(visibility=VISIBILITY_VISIBLE).first()
    else:
        return model.query.filter_by(**kwargs).first()



def query_multiple(model, **kwargs):
    # 因为传入的参数里面可能有的是None
    sorting = kwargs.pop(QUERY_ATTR_SORT_TYPE) or QUERY_SORT_TYPE_DESC  # 降序
    count = kwargs.pop(QUERY_ATTR_COUNT) or QUERY_RESULT_COUNT_DEFAULT   # 返回的数量
    # order_by 是字段名, 即表的某个字段名
    order_by = kwargs.pop(QUERY_ATTR_ORDER_BY) or  QUERY_ORDER_BY_DEFAULT   # 按照什么排序
    before_id = kwargs.pop(QUERY_ATTR_BEFORE_ID) or QUERY_BEFORE_ID_DEFAULT  # 偏移量

    field = kwargs.pop(QUERY_ATTR_FILTER_FIELD) or None
    value = kwargs.pop(QUERY_ATTR_FILTER_VALUE) or None

    # 控制查询
    query = model.query.filter_by(visibility=VISIBILITY_VISIBLE)

    # print(before_id)

    tmp = try_to_int(before_id)
    if tmp != False:
        before_id = tmp

    if before_id < 0 :
        before_id = 0

    # 用于分段获取
    query = query.filter(model.id < before_id)

    if field is not None:
        if not hasattr(model, field):
            # 即错误的参数
            return False
        query = query.filter(getattr(model, field) == value)

    if count <= 0 :
        count = QUERY_RESULT_COUNT_DEFAULT

    if not hasattr(model, order_by):
        return False

    if sorting == QUERY_SORT_TYPE_DESC:
        query = query.order_by(getattr(model, order_by).desc())
    else:
        query = query.order_by(getattr(model, order_by).asc())

    query = query.limit(count)


    # if sorting == QUERY_SORT_TYPE_DESC:
    #     return model.query.filter_by(visibility=VISIBILITY_VISIBLE).filter(model.id < before_id).order_by(getattr(model, order_by).desc()).limit(count).all()
    # else:
    #     return model.query.filter_by(visibility=VISIBILITY_VISIBLE).filter(model.id < before_id).order_by(getattr(model, order_by).asc()).limit(count).all()
    return query.all()

def query_one_to_many(model, **kwargs):
    # 因为传入的参数里面可能有的是None
    sorting = kwargs.pop(QUERY_ATTR_SORT_TYPE) or QUERY_SORT_TYPE_DESC  # 降序
    count = kwargs.pop(QUERY_ATTR_COUNT) or QUERY_RESULT_COUNT_DEFAULT   # 返回的数量
    order_by = kwargs.pop(QUERY_ATTR_ORDER_BY) or  QUERY_ORDER_BY_DEFAULT   # 按照什么排序
    before_id = kwargs.pop(QUERY_ATTR_BEFORE_ID) or QUERY_BEFORE_ID_DEFAULT  # 偏移量
    filed = kwargs.pop(QUERY_ATTR_FILTER_FIELD) or None
    value = kwargs.pop(QUERY_ATTR_FILTER_VALUE) or None

    # 如果可以转换成数字就转换为数字
    tmp = try_to_int(value)
    if tmp != False:
        value = tmp

    tmp = try_to_int(before_id)
    if tmp != False:
        before_id = tmp

    if filed is None:
        return False

    if not hasattr(model, filed) or not hasattr(model, order_by):
        # print("model has not ", filed)
        return False

    # print(model.__tablename__, " has ", filed)

    # print(before_id)

    if sorting == QUERY_SORT_TYPE_DESC:
        return \
            model.query.filter(getattr(model, filed) == value).filter(model.id < before_id).filter_by(visibility=VISIBILITY_VISIBLE).order_by(getattr(model, order_by).desc()).limit(count).all()
    else:
        return \
            model.query.filter(getattr(model, filed) == value).filter(model.id < before_id).filter_by(visibility=VISIBILITY_VISIBLE).order_by(getattr(model, order_by).asc()).limit(count).all()


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

    # print(kwargs)

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

def get_latest_id(model):
    """
    获取数据库表的最新插入项的id
    :param model: 代表数据库表
    :return: id or None
    """

    if hasattr(model, "visibility"):
        return model.query.with_entities(model.id).filter_by(visibility=VISIBILITY_VISIBLE).order_by(model.id.desc()).limit(1).first()
    else:
        return model.query.with_entities(model.id).order_by(model.id.desc()).limit(1).first()

def new_record(db, model, **kwargs):
    # print(kwargs)
    thing = model(**kwargs)
    result = add_to_db(db, thing)
    if result == True:
        if issubclass(model, Comment):
            print("generating unread messages")
            if new_unread(kwargs["post_id"], kwargs["uid"]):
                print("succeed to generate unread messages")
            else:
                print("fail to generate unread messages")

        return get_last_inserted_id(model)
    else:
        return False

def delete_from_db(db, model, id, uid):
    """
    伪删除, 把数据的 visibility 改为 INVISIBLE
    :param db:
    :param model:
    :param id:
    :param uid:
    :return:
    """
    thing = query_single_by_id(model, id)
    the_user = query_single_by_id(User, uid)
    # print(thing)
    # print(the_user)
    if thing is None or the_user is None:
        return False, ERROR_NOT_FOUND
    # print("checking")
    # 检查有没有权限删除
    if thing.uid != uid and not the_user.account in config["ADMINISTRATION"]:
        return False, ERROR_USER_ID_CONFLICT
    try:
        if hasattr(thing, "visibility"):
            thing.visibility = VISIBILITY_INVISIBLE
            db.session.add(thing)
        else:   # 确实删除
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
            # print("token is right")
            return True
        else:
            print("token wrong {}".format(token))
    return False