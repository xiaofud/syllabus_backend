# coding=utf-8
__author__ = 'smallfly'

from flask_restful import fields, reqparse
from app.mod_interaction.resources.GenericResource import GenericResource
from app.mod_interaction.database_operations import post_operation
from app.mod_interaction.models import Post

structure = {
    "id": fields.Integer,
    "post_type": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "post_time": fields.String,
    "uid": fields.Integer,
    "description": fields.String
}

basic_parser = reqparse.RequestParser(trim=True)
# 之后要加上token验证
basic_parser.add_argument("title", required=True, location="json")
basic_parser.add_argument("content", required=True, location="json")
basic_parser.add_argument("description", location="json")
basic_parser.add_argument("uid", type=int, required=True, location="json")
basic_parser.add_argument("post_type", type=int, required=True, location="json")
basic_parser.add_argument("token", required=True, location="json")

# 需要提交之前修改的id
put_parser = basic_parser.copy()
put_parser.add_argument("id", type=int, required=True, location="json")

delete_parser = reqparse.RequestParser(trim=True)
delete_parser.add_argument("token", required=True, location="json")
delete_parser.add_argument("uid", required=True, location="json")

# 新的对象的参数
POST_ACCEPT_VARIABLES = ("title", "content", "description", "uid", "post_type", "token")

# 用于修改之前post过的数据
PUT_ACCEPT_VARIABLES = ("title", "content", "description", "uid", "post_type", "id", "token")

# POST_RESOURCE_ACCEPTED_VARIABLE_DICT = {
#     "post": POST_ACCEPT_VARIABLES,
#     "put": PUT_ACCEPT_VARIABLES
# }

INITIAL_KWARGS = {
    GenericResource.ACCEPTED_VARIABLE_DICT: {
        "post": POST_ACCEPT_VARIABLES,
        "put": PUT_ACCEPT_VARIABLES
    },
    GenericResource.MARSHAL_STRUCTURE: structure,
    GenericResource.PARSERS_FOR_METHOD:{
        "post": basic_parser,
        "put": put_parser,
        "delete": delete_parser
    },
    GenericResource.MODEL: Post,
    GenericResource.RESOURCE_NAME: "post",
    GenericResource.TOKEN_CHECK_FOR_METHODS_DICT:{
        "post": post_operation.check_token,
        "delete": post_operation.check_token
    }
}

# class PostResource(Resource):
#
#
#
#     def get(self, id=None):
#         if id is None:
#             return {"error": "bad request"}, 401
#         post = post_operation.get_post_by_id(id)
#         if post is None:
#             return {"error": "invalid id"}, 404    # not found
#         return marshal(post, structure), 200
#
#     # curl localhost:8080/interaction/api/v2/post -i --header "Content-type: application/json" -X POST -d '{"title": "testing_title", "content": "haha", "description": "click me", "uid": 1, "post_type": 1}'
#     def post(self):
#         args = basic_parser.parse_args()
#         helpers.clean_arguments(args, PostResource.POST_ACCEPT_VARIABLES)
#         result = post_operation.new_post(**args)
#         if result != False:
#             return {"id": result}, 201  # crated
#         else:
#             return {"error": "failed"}, 500 # Internal Server Error
#
#     # curl localhost:8080/interaction/api/v2/post -i --header "Content-type: application/json" -X PUT -d '{"title": "testing_title", "content": "haha", "id": 2, "description": "do not click me", "uid": 1, "post_type": 1}'
#     def put(self):
#         args = put_parser.parse_args()
#         helpers.clean_arguments(args, PostResource.PUT_ACCEPT_VARIABLES)
#         id = args.pop("id")
#         result = post_operation.update_post_by_id(id, **args)
#         if result == True:
#             return {"status": "updated"}, 200
#         else:
#             if result[1] == post_operation.common.ERROR_NOT_FOUND:
#                 return {"error": "post not found"}, 404
#             else:
#                 return {"error": "failed"}, 500 # Internal Server Error


