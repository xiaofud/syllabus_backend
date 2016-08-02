# coding=utf-8


__author__ = 'smallfly'

from flask_restful import fields, reqparse
from app.mod_interaction.resources.GenericSingleResource import GenericSingleResource
from app.mod_interaction.resources.GenericMultipleResource import GenericMultipleResource
from app.mod_interaction.database_operations import common
from app.mod_interaction.models import Post
# from app.mod_interaction.resources import ThumbUpResource

thumb_ups_structure = {
    "id": fields.Integer,   # 该赞的id, 方便用于取消
    "uid": fields.Integer,  # 点赞的人
}

comment_structure = {
    "id": fields.Integer,   # 评论的id, 用于删除
    "uid": fields.Integer,  # 发布评论的用户id
}

user_structure = {
    "id": fields.Integer,
    "image": fields.String,
    "nickname": fields.String,
    "account": fields.String
}

SINGLE_POST_STRUCTURE = {
    "id": fields.Integer,
    "post_type": fields.Integer,
    # "title": fields.String,
    "content": fields.String,
    "post_time": fields.String,
    "source":fields.String,
    "user": fields.Nested(user_structure),
    "description": fields.String,
    "thumb_ups": fields.List(fields.Nested(thumb_ups_structure)),
    "comments": fields.List(fields.Nested(comment_structure)),
    "photo_list_json": fields.String
}

post_parser = reqparse.RequestParser(trim=True)
# post_parser.add_argument("title", required=True, location="json")
post_parser.add_argument("source", location="json")
post_parser.add_argument("content", required=True, location="json")
post_parser.add_argument("uid", type=int, required=True, location="json")
post_parser.add_argument("post_type", type=int, required=True, location="json")
post_parser.add_argument("token", required=True, location="json")
post_parser.add_argument("description", location="json")
post_parser.add_argument("photo_list_json", location="json")

# 必须的参数 content, uid, post_type, token
# 非必须参数 description photo_list_json

# 需要提交之前修改的id
put_parser = post_parser.copy()
put_parser.add_argument("id", type=int, required=True, location="json")

delete_parser = reqparse.RequestParser(trim=True)
delete_parser.add_argument("token", required=True, location="headers")
delete_parser.add_argument("uid", type=int, required=True, location="headers")
delete_parser.add_argument("id", type=int, required=True, location="headers")

# 新的对象的参数
SINGLE_POST_ACCEPT_VARIABLES = ("content", "description", "uid", "post_type", "token", "photo_list_json", "source")

# 用于修改之前post过的数据
SINGLE_PUT_ACCEPT_VARIABLES = ("content", "description", "uid", "post_type", "id", "token", "photo_list_json", "source")

# POST_RESOURCE_ACCEPTED_VARIABLE_DICT = {
#     "post": POST_ACCEPT_VARIABLES,
#     "put": PUT_ACCEPT_VARIABLES
# }

SINGLE_INITIAL_KWARGS = {
    GenericSingleResource.ACCEPTED_VARIABLE_DICT: {
        "post": SINGLE_POST_ACCEPT_VARIABLES,
        "put": SINGLE_PUT_ACCEPT_VARIABLES
    },
    GenericSingleResource.MARSHAL_STRUCTURE: SINGLE_POST_STRUCTURE,
    GenericSingleResource.PARSERS_FOR_METHOD:{
        "post": post_parser,
        "put": put_parser,
        "delete": delete_parser
    },
    GenericSingleResource.MODEL: Post,
    GenericSingleResource.RESOURCE_NAME: "post",
    GenericSingleResource.TOKEN_CHECK_FOR_METHODS_DICT:{
        "post": common.check_token,
        "delete": common.check_token,
        "put": common.check_token
    }
    ,
    # GenericResource.RESOURCE_GETTER: common.query_single_by_id
}

# 获取文章列表

get_multiple_posts_parser = reqparse.RequestParser(trim=True)
get_multiple_posts_parser.add_argument(common.QUERY_ATTR_COUNT, type=int, location="args")
get_multiple_posts_parser.add_argument(common.QUERY_ATTR_ORDER_BY, location="args")
get_multiple_posts_parser.add_argument(common.QUERY_ATTR_SORT_TYPE, type=int, location="args")    # 1 表示升序, 2 表示降序
get_multiple_posts_parser.add_argument(common.QUERY_ATTR_BEFORE_ID, type=int, location="args")
get_multiple_posts_parser.add_argument(common.QUERY_ATTR_FILTER_FIELD, location="args")
get_multiple_posts_parser.add_argument(common.QUERY_ATTR_FILTER_VALUE, location="args")



# 这里不需要单独写一个多用户的 marshal 结构, 解释如下
# https://github.com/flask-restful/flask-restful/issues/300
# MULTIPLE_USERS_STRUCTURE = {
#     "user_list": fields.List(fields.Nested(SINGLE_USER_STRUCTURE))
#     # "user": fields.Nested(SINGLE_USER_STRUCTURE)
# }

MULTIPLE_USERS_INITIAL_KWARGS = {
    GenericMultipleResource.MARSHAL_STRUCTURE: SINGLE_POST_STRUCTURE,
    GenericMultipleResource.MODEL: Post,
    GenericMultipleResource.PARSER_FOR_METHODS_DICT: {
        "get": get_multiple_posts_parser
    },
    GenericMultipleResource.ENVELOPE: "post_list"
}



