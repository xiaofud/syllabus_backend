# coding=utf-8
__author__ = 'xiaofud'

from flask_restful import Resource, reqparse
from app.mod_interaction.models import Post
from app.mod_interaction.database_operations import common
from app import db


post_parser = reqparse.RequestParser(trim=True)

post_parser.add_argument("source", location="json")
post_parser.add_argument("content", required=True, location="json")
# post_parser.add_argument("uid", type=int, required=True, location="json")
# post_parser.add_argument("post_type", type=int, required=True, location="json")
# post_parser.add_argument("token", required=True, location="json")
post_parser.add_argument("description", location="json")
post_parser.add_argument("photo_list_json", location="json")

class AnonymousResource(Resource):
    """
    发布匿名消息，全部归结为user id为-1的固定用户
    """

    USER_ID = -1
    POST_TYPE = Post.POST_TYPE_ANONYMOUS

    def post(self):
        args = post_parser.parse_args()
        # 添加一些固定的值
        args["uid"] = AnonymousResource.USER_ID
        args["post_type"] = AnonymousResource.POST_TYPE
        result = common.new_record(db, Post, **args)
        if result:
            return {"id": result}, 201  # crated
        else:
            return {"error": "failed"}, 500 # Internal Server Error