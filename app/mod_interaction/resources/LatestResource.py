# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, reqparse
from flask import jsonify
from app.mod_interaction.database_operations import common
from app.mod_interaction.models import Post, User

class LatestResource(Resource):

    GET_PARSER = reqparse.RequestParser(trim=True)
    MODEL_TYPE_USER = 0
    MODEL_TYPE_POST = 1

    def get(self):
        """
        curl localhost:8080/interaction/api/v2/latest
        可选参数, type, 指定查询的表,
        MODEL_TYPE_USER = 0, 用户
        MODEL_TYPE_POST = 1, post表
        返回值是{"id": "id"} 类型, id值可能是None
        :return:
        """
        self.GET_PARSER.add_argument("type", location="args")
        args = self.GET_PARSER.parse_args()
        # 默认是查询post数据

        type_ = args["type"] or self.MODEL_TYPE_POST
        if type_ == self.MODEL_TYPE_POST:
            model = Post
        elif type_ == self.MODEL_TYPE_USER:
            model = User
        else:
            return jsonify(error="invalid type")
        id_ = common.get_latest_id(model)
        if id_ is not None:
            return jsonify(id=id_.id)
        else:
            return jsonify(id=None)