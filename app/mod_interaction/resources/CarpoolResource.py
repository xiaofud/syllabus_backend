# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, fields, marshal
from flask_restful.reqparse import RequestParser
from app.mod_interaction.database_operations import common
from app.mod_interaction import models
from app.mod_interaction.resources.helpers import timestamp_to_string
from app.mod_interaction.resources import PassengerResource
from app import db

CARPOOL_STRUCTURE = {
    "id": fields.Integer,
    "uid": fields.Integer,
    "departure_time": fields.String,
    "driver": fields.String,
    "contact": fields.String,
    "source": fields.String,
    "destination": fields.String,
    "notice": fields.String,
    "max_people": fields.Integer,
    "people_count": fields.Integer,
    "passengers": fields.List(fields.Nested(PassengerResource.PASSENGER_STRUCTURE))
}

class CarpoolResource(Resource):

    """
    单个拼车信息
    """

    GET_PARSER = RequestParser(trim=True)
    POST_PARSER = RequestParser(trim=True)

    def get(self):
        self.GET_PARSER.add_argument("id", required=True, type=int, location="args")
        args = self.GET_PARSER.parse_args()
        id_ = args['id']
        carpool = common.query_single_by_id(models.Carpool, id_)
        if carpool is not None:
            return marshal(carpool, CARPOOL_STRUCTURE)
        else:
            return {"error": "not found"}, 404


    def post(self):

        # 验证信息
        self.POST_PARSER.add_argument("uid", type=int, required=True, location="form")
        self.POST_PARSER.add_argument("token", required=True, location="form")
        # 具体数据
        self.POST_PARSER.add_argument("departure_time", type=int, required=True, location="form")
        self.POST_PARSER.add_argument("driver", required=True, location="form")
        self.POST_PARSER.add_argument("contact", required=True, location="form")
        self.POST_PARSER.add_argument("source", required=True, location="form")
        self.POST_PARSER.add_argument("destination", required=True, location="form")
        self.POST_PARSER.add_argument("notice", required=False, location="form")
        self.POST_PARSER.add_argument("max_people", required=True, location="form")
        # self.POST_PARSER.add_argument("people_count")

        args = self.POST_PARSER.parse_args()

        # 检查token
        if not common.check_token(args):
            return {"error": "wrong token"}, 401

        del args["token"]

        args["departure_time"] = timestamp_to_string(args["departure_time"])

        carpool = models.Carpool(**args)
        # print(carpool)
        if common.add_to_db(db, carpool) == True:
            return {"id": common.get_last_inserted_id(models.Carpool)}, 200
        else:
            return {"error": "Internal Server Error"}, 500



class CarpoolsResource(Resource):
    """
    获取多个拼车消息
    """

    # 有无司机
    HAS_DRIVER = 1
    HAS_NOT_DRIVER = 2

    GET_PARSER = RequestParser(trim=True)

    def get(self):
        """
        可有多种条件组合搜索, 注意排序
        时间|有无司机|人数
        :return:
        """
        self.GET_PARSER.add_argument("depart_time", type=int, location="args")
        self.GET_PARSER.add_argument("driver", type=int, location="args")
        # 已经有的人数
        self.GET_PARSER.add_argument("count", type=int, location="args")
        # 用于分页
        self.GET_PARSER.add_argument("before_id", type=int, location="args")
        # 用于分页
        self.GET_PARSER.add_argument("page_size", type=int, location="args")

        # 排序相关
        # 排序关键字
        self.GET_PARSER.add_argument("sort_by", action="append", location="args")
        # 排序顺序
        self.GET_PARSER.add_argument("order", action="append", location="args")

        args = self.GET_PARSER.parse_args()
        return args
