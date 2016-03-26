# coding=utf-8
__author__ = 'smallfly'

from flask_restful import fields, reqparse, Resource, marshal
from app.mod_interaction.models import User
from app.mod_interaction.database_operations import common
from app.mod_interaction.resources.GenericSingleResource import GenericSingleResource
from app.mod_interaction.resources.GenericMultipleResource import  GenericMultipleResource

SINGLE_USER_STRUCTURE = {
    "id": fields.Integer,
    "account": fields.String,
    "nickname": fields.String,
    "gender": fields.Integer,
    "birthday": fields.String,
    "profile": fields.String,
    "image": fields.String
    # "token": fields.String
    # "thumb_ups": fields.List(fields.Nested(ThumbUpResource.structure))
}

# 验证参数
put_parser = reqparse.RequestParser(trim=True)
put_parser.add_argument("id", type=int, required=True, location='json')
put_parser.add_argument("uid", type=int, required=True, location="json")
put_parser.add_argument("token", required=True, location='json')
put_parser.add_argument("nickname", location='json')
# 使用时间戳
put_parser.add_argument("birthday", type=int, location='json')
put_parser.add_argument("profile", location='json')
put_parser.add_argument("gender", location='json')

# 头像
put_parser.add_argument("image", location="json")

SINGLE_USER_PUT_ACCEPT_VARIABLES = ("id", "nickname", "birthday", "profile", "gender", "uid", "token")

SINGLE_USER_INITIAL_KWARGS = {
    GenericSingleResource.MODEL: User,
    GenericSingleResource.PARSERS_FOR_METHOD: {
        "put": put_parser
    },
    GenericSingleResource.MARSHAL_STRUCTURE: SINGLE_USER_STRUCTURE,
    GenericSingleResource.RESOURCE_NAME: "user",
    GenericSingleResource.ACCEPTED_VARIABLE_DICT: {
        "put": SINGLE_USER_PUT_ACCEPT_VARIABLES
    },
    GenericSingleResource.TIMESTAMP_TO_STRING_LIST: [
      "birthday"
    ],
    GenericSingleResource.NOT_ALLOWED_METHODS_LIST: [
        "delete", "post"
    ],
    GenericSingleResource.TOKEN_CHECK_FOR_METHODS_DICT:{
        "put": common.check_token
    }
}

# 获取用户列表

get_multiple_users_parser = reqparse.RequestParser(trim=True)
get_multiple_users_parser.add_argument(common.QUERY_ATTR_COUNT, type=int, location="args")
get_multiple_users_parser.add_argument(common.QUERY_ATTR_ORDER_BY, location="args")
get_multiple_users_parser.add_argument(common.QUERY_ATTR_SORT_TYPE, type=int, location="args")    # 1 表示升序, 2 表示降序
get_multiple_users_parser.add_argument(common.QUERY_ATTR_OFFSET, type=int, location="args")



# 这里不需要单独写一个多用户的 marshal 结构, 解释如下
# https://github.com/flask-restful/flask-restful/issues/300
# MULTIPLE_USERS_STRUCTURE = {
#     "user_list": fields.List(fields.Nested(SINGLE_USER_STRUCTURE))
#     # "user": fields.Nested(SINGLE_USER_STRUCTURE)
# }

MULTIPLE_USERS_INITIAL_KWARGS = {
    GenericMultipleResource.MARSHAL_STRUCTURE: SINGLE_USER_STRUCTURE,
    GenericMultipleResource.MODEL: User,
    GenericMultipleResource.PARSER_FOR_METHODS_DICT: {
        "get": get_multiple_users_parser
    },
    GenericMultipleResource.ENVELOPE: "user_list"
}

class CompatibleUserResource(Resource):
    """
    因为之前服务器上使用的是用户账号来获取和修改数据, 所以这里要写一个向前兼容的api
    """

    # account 那里一定要用urlencode编码过后才能加在url后
    def get(self, account=None):
        if account is None:
            return {"error": "name required in the query parameter"}, 400
        # print(name)
        # input()
        user = common.query_single_by_filed(User, "account", account)
        if user is None:
            return {"error": "no user's account is {}".format(account)}, 404
        return marshal(user, SINGLE_USER_STRUCTURE)

# class UserResource(GenericResource):
#
#     # curl --header "Content-type: application/json" localhost:8080/interaction/api/v2/user -X PUT -d '{"id": 1, "birthday": "819648000", "nickname": "xiaofud", "gender": 1, "profile": "hello world"}'
#     # date -d "1995-12-23" "+%s"    获取时间戳
#     def put(self):
#         args = put_parser.parse_args()
#         if args["birthday"] is not None:
#             birthday = datetime.fromtimestamp(int(args["birthday"]))
#             birthday = birthday.strftime("%Y-%m-%d %H:%M:%S")
#             args["birthday"] = birthday
#             # print(birthday)
#         user_id = args.pop("id")
#
#         # for arg in args:
#         #     if arg not in UserResource.ACCEPT_VARIABLES:
#         #         args.pop(arg)
#         # 去除其他参数, 避免用户自己修改token之类的数据
#         helpers.clean_arguments(args, PUT_ACCEPT_VARIABLES)
#
#         result = user_operation.update_user_by_id(user_id, **args)
#         if result == True:
#             return {"status": "updated"}, 200
#         else:
#             if result[1] == user_operation.common.ERROR_NOT_FOUND:
#                 return {"error": "user not found"}, 404
#             else:
#                 return {"error": "failed"}, 500 # Internal Server Error



# Argument Locations
# By default, the RequestParser tries to parse values from flask.Request.values, and flask.Request.json.
#
# Use the location argument to add_argument() to specify alternate locations to pull the values from. Any variable on the flask.Request can be used. For example:
#
# # Look only in the POST body
# parser.add_argument('name', type=int, location='form')
#
# # Look only in the querystring
# parser.add_argument('PageSize', type=int, location='args')
#
# # From the request headers
# parser.add_argument('User-Agent', location='headers')
#
# # From http cookies
# parser.add_argument('session_id', location='cookies')
#
# # From file uploads
# parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
# Note
# Only use type=list when location='json'. See this issue for more details