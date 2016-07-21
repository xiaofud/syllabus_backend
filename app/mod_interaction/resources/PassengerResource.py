# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, fields, marshal
from flask_restful.reqparse import RequestParser
from app.mod_interaction.database_operations import common
from app.mod_interaction import models
from app.mod_interaction.resources import helpers
from app import db

import time

PASSENGER_STRUCTURE = {
    # # 主键
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #
    # # 发起拼车的童鞋
    # uid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    #
    # # 拼车信息id
    # carpool_id = db.Column(db.Integer, db.ForeignKey("carpools.id"), nullable=False)
    #
    # # join time
    # join_time = db.Column(db.TIMESTAMP, default=None)
    #
    # # 自己的联系方式(用json方式存储)
    # contact = db.Column(db.VARCHAR(200), nullable=True)

    "id": fields.Integer,
    "uid": fields.Integer,
    "carpool_id": fields.Integer,
    "join_time": fields.String,
    "contact": fields.String
}

class PassengerResource(Resource):

    GET_PARSER = RequestParser(trim=True)
    POST_PARSER = RequestParser(trim=True)
    PUT_PARSER = RequestParser(trim=True)
    DELETE_PARSER = RequestParser(trim=True)

    def get(self):
        self.GET_PARSER.add_argument("id", required=True, type=int, location="args")

        args = self.GET_PARSER.parse_args()
        id_ = args["id"]
        passenger = common.query_single_by_id(models.Passenger, id_)
        if passenger is None:
            return {"error": "not found"}, 404
        return marshal(passenger, PASSENGER_STRUCTURE)

    def post(self):
        self.POST_PARSER.add_argument("contact", required=True, location="form")
        # self.POST_PARSER.add_argument("id", type=int, required=True, location="form")
        self.POST_PARSER.add_argument("carpool_id", type=int, required=True, location="form")

        self.POST_PARSER.add_argument("uid", type=int, required=True, location="form")
        self.POST_PARSER.add_argument("token", required=True, location="form")

        args = self.POST_PARSER.parse_args()

        # 检查token
        if not common.check_token(args):
            return {"error": "wrong token"}, 401

        del args["token"]

        # 检查carpool存不存在
        carpool = common.query_single_by_id(models.Carpool, args["carpool_id"])
        if carpool is None:
            return {"error": "carpool not exists"}, 404

        # 不允许加入几次拼车
        passenger = models.Passenger.query.filter_by(uid=args["uid"]).filter_by(carpool_id=carpool.id).first()

        if passenger is not None:
            return {"error": "already in this carpool"}, 400

        # 加入时间戳
        args["join_time"] = helpers.timestamp_to_string(int(time.time()))
        passenger = models.Passenger(**args)

        count = carpool.people_count + 1
        if count > carpool.max_people:
            return {"error": "people overflows"}, 400

        carpool.people_count = count

        if common.add_to_db(db, passenger) == True and common.add_to_db(db, carpool) == True:
            return {"id": common.get_last_inserted_id(models.Passenger)}, 200
        else:
            return {"error": "Internal Server Error"}, 500

    def put(self):
        # 用于更新信息, 只允许修改contact信息
        self.PUT_PARSER.add_argument("id", type=int, required=True, location="form")
        # self.PUT_PARSER.add_argument("carpool_id", type=int, required=True, location="form")
        self.PUT_PARSER.add_argument("uid", type=int, required=True, location="form")
        self.PUT_PARSER.add_argument("token", required=True, location="form")
        self.PUT_PARSER.add_argument("contact", required=True, location="form")

        args = self.PUT_PARSER.parse_args()

        # 检查token
        if not common.check_token(args):
            return {"error": "wrong token"}, 401

        # passenger = models.Passenger.query.filter_by(uid=args["uid"]).filter_by(carpool_id=args["carpool_id"]).first()
        passenger = models.Passenger.query.filter_by(id=args["id"]).first()
        # 并未上车
        if passenger is None:
            return {"error": "passenger not exists"}, 404

        passenger.contact = args["contact"]

        if common.add_to_db(db, passenger) == True:
            return {"status": "updated"}, 200
        else:
            return {"error": "Internal Server Error"}, 500

    def delete(self):
        self.DELETE_PARSER.add_argument("id", type=int, required=True, location="headers")
        self.DELETE_PARSER.add_argument("uid", type=int, required=True, location="headers")
        self.DELETE_PARSER.add_argument("token", required=True, location="headers")

        args = self.DELETE_PARSER.parse_args()

        # 检查token
        if not common.check_token(args):
            return {"error": "wrong token"}, 401

        # passenger = models.Passenger.query.filter_by(id=args["id"]).first()
        # # 并未上车
        # if passenger is None:
        #     return {"error": "passenger not exists"}, 404
        status = common.delete_from_db(db, models.Passenger, args["id"], args["uid"])
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