# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.mod_interaction.database_operations import common
from app.mod_interaction import models
from app import db
import random

NUMBERS = [str(i) for i in range(10)]

def generate_collection_id(length=6):
    collection_id = ""
    for i in range(length):
        collection_id += random.choice(NUMBERS)
    return collection_id

def check_existence(collection_id):
    collector = common.query_single_by_filed(models.Collector, "collection_id", collection_id)
    if collector is None:
        return False
    return True


class CollectorResource(Resource):
    """
    用于申请课表收集的API
    """

    POST_PARSER = RequestParser(trim=True)
    GET_PARSER = RequestParser(trim=True)

    def get(self):
        self.GET_PARSER.add_argument("username", required=True, location="headers")
        self.GET_PARSER.add_argument("token", required=True, location="headers")

        args = self.GET_PARSER.parse_args()
        user = common.query_single_by_filed(models.User, "account", args["username"])
        if user is None:
            return {"error": "user doesn't exist"}, 404
        token_check = {
            "uid": user.id,
            "token": args["token"]
        }
        if not common.check_token(token_check):
            return {"error": "token is wrong"}, 401

        collectors = models.Collector.query.filter_by(uid=user.id).all()
        result = []
        for collector in collectors:
            count = models.SyllabusCollection.query.with_entities(models.SyllabusCollection.collection_id).filter_by(collection_id=collector.collection_id).count()
            result.append(
                {
                    "collection_id": collector.collection_id,
                    "start_year": collector.start_year,
                    "season": collector.season,
                    "count": count
                }
            )
        # collectors = [ dict(collection_id=x.collection_id, start_year=x.start_year, season=x.season) for x in collectors ]

        return {"collection_ids": result}

    def post(self):
        """
        请求地址: /interaction/api/v2/collector
        参数:
            必选参数:
            位置: form
                username 用户账号
                token 用户验证令牌
                start_year 学年的开始年份
                season 春夏秋指定一个, 同学分制
        :return:
        """
        self.POST_PARSER.add_argument("username", required=True, location="form")
        self.POST_PARSER.add_argument("token", required=True, location="form")
        self.POST_PARSER.add_argument("start_year", type=int, required=True, location="form")
        self.POST_PARSER.add_argument("season", type=int, required=True, location="form")

        args = self.POST_PARSER.parse_args()
        user = common.query_single_by_filed(models.User, "account", args["username"])
        if user is None:
            return {"error": "user doesn't exist"}, 404
        token_check = {
            "uid": user.id,
            "token": args["token"]
        }
        if not common.check_token(token_check):
            return {"error": "token is wrong"}, 401

        while True:
            collection_id = generate_collection_id()
            if not check_existence(collection_id):
                break

        collector = models.Collector(collection_id=collection_id, start_year=args["start_year"], season=args["season"], uid=user.id)
        result = common.add_to_db(db, collector)
        if result == True:
            return {"collection_id": collector.collection_id}
        else:
            return {"error": "commit error in mysql"}, 500



