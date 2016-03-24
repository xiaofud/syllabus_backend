# coding=utf-8
__author__ = 'smallfly'

from flask_restful import reqparse, fields
from app.mod_interaction.resources.GenericSingleResource import GenericSingleResource
from app.mod_interaction.resources.GenericOneToManyRelationResource import GenericOneToManyRelationResource
from app.mod_interaction.database_operations import common
from app.mod_interaction.models import Comment

SINGLE_COMMENT_STRUCTURE = {
    "id": fields.Integer,
    "post_time": fields.String,
    "comment": fields.String,
    "post_id": fields.Integer,
    "uid": fields.Integer
}

post_parser = reqparse.RequestParser(trim=True)
post_parser.add_argument("post_id", required=True, type=int, location="json")
post_parser.add_argument("uid", required=True, type=int, location="json")
post_parser.add_argument("comment", required=True, location="json")
post_parser.add_argument("token", required=True, location="json")


put_parser = post_parser.copy()
put_parser.add_argument("id", required=True, type=int, location="json")

delete_parser = reqparse.RequestParser(trim=True)
delete_parser.add_argument("uid", required=True, type=int, location="json")
delete_parser.add_argument("token", required=True, location="json")
delete_parser.add_argument("id", required=True, type=int, location="json")

SINGLE_USER_INITIAL_KWARGS = {
    GenericSingleResource.ACCEPTED_VARIABLE_DICT: {
        "put": ["id", "post_id", "uid", "comment", "token"],
        "post": ["post_id", "uid", "comment", "token"],
    },
    GenericSingleResource.MARSHAL_STRUCTURE: SINGLE_COMMENT_STRUCTURE,
    GenericSingleResource.MODEL:Comment,
    GenericSingleResource.RESOURCE_NAME: "comment",
    GenericSingleResource.PARSERS_FOR_METHOD:{
        "post": post_parser,
        "put": put_parser,
        "delete": delete_parser
    },
    GenericSingleResource.TOKEN_CHECK_FOR_METHODS_DICT:{
        "post": common.check_token,
        "put": common.check_token,
        "delete": common.check_token
    }
}

# 查找属于某个post的所有评论

get_comments_parser = reqparse.RequestParser(trim=True)
# 必须参数
# 比较的字段
get_comments_parser.add_argument(common.QUERY_ATTR_FILTER_FIELD, required=True, location="args")
get_comments_parser.add_argument(common.QUERY_ATTR_FILTER_VALUE, required=True, location="args")

# 处理结果的可选参数
get_comments_parser.add_argument(common.QUERY_ATTR_COUNT, type=int, location="args")
get_comments_parser.add_argument(common.QUERY_ATTR_ORDER_BY, location="args")
get_comments_parser.add_argument(common.QUERY_ATTR_SORT_TYPE, type=int, location="args")    # 1 表示升序, 2 表示降序
get_comments_parser.add_argument(common.QUERY_ATTR_OFFSET, type=int, location="args")


QUERY_COMMENTS_FOR_POST_INITIAL_KWARGS = {
    GenericOneToManyRelationResource.PARSER_FOR_METHODS_DICT:{
        "get": get_comments_parser
    },
    GenericOneToManyRelationResource.MARSHAL_STRUCTURE: SINGLE_COMMENT_STRUCTURE,
    GenericOneToManyRelationResource.ENVELOPE: "comments",
    GenericOneToManyRelationResource.MODEL: Comment,
}