# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, fields, marshal
from flask_restful.reqparse import RequestParser
from app.mod_interaction.database_operations import common
from app.mod_interaction import models
from app.mod_interaction.resources.helpers import timestamp_to_string
from app.mod_interaction.resources import PassengerResource
from app import db

import time

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
    PUT_PARSER = RequestParser(trim=True)
    DELETE_PARSER = RequestParser(trim=True)

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
            # 这里还要添加一条记录到 Passenger 里
            now = timestamp_to_string(int(time.time()))
            passenger = models.Passenger(join_time=now,
                                         uid=args["uid"],
                                         carpool_id=carpool.id,
                                         contact=args["contact"]
            )
            common.add_to_db(db, passenger)
            return {"id": carpool.id}, 200
        else:
            return {"error": "Internal Server Error"}, 500

    def put(self):
        # 验证信息
        self.PUT_PARSER.add_argument("uid", type=int, required=True, location="form")
        self.PUT_PARSER.add_argument("token", required=True, location="form")
        # 具体数据
        self.PUT_PARSER.add_argument("departure_time", type=int, required=True, location="form")
        self.PUT_PARSER.add_argument("driver", required=True, location="form")
        self.PUT_PARSER.add_argument("contact", required=True, location="form")
        self.PUT_PARSER.add_argument("source", required=True, location="form")
        self.PUT_PARSER.add_argument("destination", required=True, location="form")

        self.PUT_PARSER.add_argument("notice", required=False, location="form")

        self.PUT_PARSER.add_argument("max_people", required=True, location="form")

        self.PUT_PARSER.add_argument("id", type=int, required=True, location="form")

        args = self.PUT_PARSER.parse_args(strict=True)
        # print(args)
        # 检查token
        if not common.check_token(args):
            return {"error": "wrong token"}, 401

        # 去掉其他辅助信息
        del args["token"]

        id_ = args["id"]
        del args["id"]

        uid = args["uid"]
        del args["uid"]

        args["departure_time"] = timestamp_to_string(args["departure_time"])

        status = common.update_model_by_id(models.Carpool, db, id_, uid, **args)
        if status == True:
            return {"status": "updated"}
        else:
            code = status[1]
            if code == common.ERROR_NOT_FOUND:
                return {"error": "not found"}, 404
            elif code == common.ERROR_USER_ID_CONFLICT:
                return {"error": "forbidden"}, 403
            elif code == common.ERROR_COMMIT_FAILED:
                return {"error": "Internal Server Error"}, 500

    def delete(self):
        self.DELETE_PARSER.add_argument("id", type=int, required=True, location="headers")
        self.DELETE_PARSER.add_argument("uid", type=int, required=True, location="headers")
        self.DELETE_PARSER.add_argument("token", required=True, location="headers")

        args = self.DELETE_PARSER.parse_args()

        # 检查token
        if not common.check_token(args):
            return {"error": "wrong token"}, 401

        status = common.delete_from_db(db, models.Carpool, args["id"], args["uid"])
        if status == True:
            return {"status": "deleted"}
        else:
            code = status[1]
            if code == common.ERROR_NOT_FOUND:
                return {"error": "not found"}, 404
            elif code == common.ERROR_USER_ID_CONFLICT:
                return {"error": "forbidden"}, 403
            elif code == common.ERROR_COMMIT_FAILED:
                return {"error": "Internal Server Error"}, 500


class CarpoolSResource(Resource):
    """
    获取多个拼车消息
    """

    # 有无司机
    HAS_DRIVER = 1
    HAS_NOT_DRIVER = 2

    GET_PARSER = RequestParser(trim=True)

    def query(self, arg_dict):
        # 分页 http://my.oschina.net/ranvane/blog/196906

        # 按照各种条件搜索拼车
        # query_obj = models.Carpool.query

        # 读取条件
        now = timestamp_to_string(int(time.time()))
        # 设置时间条件
        depart_time = arg_dict["depart_time"] or now

        # print(depart_time)

        page_index = arg_dict["page_index"] or 1

        page_size = arg_dict["page_size"] or 10

        page_obj = \
            models.Carpool.query\
                .filter(models.Carpool.departure_time >= depart_time)\
                .order_by(models.Carpool.departure_time.asc())\
                .order_by(models.Carpool.people_count.desc())\
                .paginate(page_index, page_size, False)

        carpools = page_obj.items

        # print(len(carpools))

        return carpools





    def get(self):
        """
        可有多种条件组合搜索, 注意排序
        时间|有无司机|人数
        :return:
        """
        self.GET_PARSER.add_argument("depart_time", type=int, location="args")
        # DRIVER 由客户端判断
        # self.GET_PARSER.add_argument("driver", type=int, location="args")
        # 已经有的人数, 由客户端判断
        # self.GET_PARSER.add_argument("count", type=int, location="args")
        # 用于分页
        self.GET_PARSER.add_argument("page_index", type=int, location="args")
        # 用于分页
        self.GET_PARSER.add_argument("page_size", type=int, location="args")

        # 排序相关
        # 排序关键字
        # self.GET_PARSER.add_argument("sort_by", action="append", location="args")
        # 排序顺序
        # self.GET_PARSER.add_argument("order", action="append", location="args")

        args = self.GET_PARSER.parse_args()

        carpools = self.query(args)

        print(len(carpools))

        if len(carpools) > 0:
            return marshal(carpools, CARPOOL_STRUCTURE)
        else:
            return {"error": "nothing found"}, 404

