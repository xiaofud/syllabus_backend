# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.mod_interaction.database_operations import common
from app.mod_interaction import models
from app import db

class SyllabusCollectionResource(Resource):
    """
    用于记录课表
    """

    POST_PARSER = RequestParser(trim=True)
    GET_PARSER = RequestParser(trim=True)

    def get(self):
        """
        申请人获取用户已经上传的课表数据
        地址: /interaction/api/v2/syllabus_collection
        方法: GET
        参数:
            位置: headers
            必须参数:
                username 用户账号
                token 验证令牌
                collectionID 之前申请到的获取id
        :return:
        """
        self.GET_PARSER.add_argument("username", required=True, location="headers")
        self.GET_PARSER.add_argument("token", required=True, location="headers")
        # header里面的键名不能有下划线
        self.GET_PARSER.add_argument("collectionID", required=True, location="headers")

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

        collector = common.query_single_by_filed(models.Collector, "collection_id", args["collectionID"])
        if collector is None:
            # 表明用户输入了错误的collection_id
            return {"error": "wrong collection_id"}, 404

        # 检查权限
        if collector.uid != user.id:
            return {"error": "have not the permission"}, 403

        collections = models.SyllabusCollection.query.filter_by(collection_id=args["collectionID"]).all()
        collections = [ dict(account=x.account, syllabus=x.syllabus) for x in collections ]
        return {"collections": collections}


    def post(self):
        """
        发送课表数据到服务器
        地址: /interaction/api/v2/syllabus_collection
        方法: POST
        参数:
            位置: form
            必选参数:
                username 用户账号
                token 验证令牌
                start_year 学年的开始年份
                season 某个学期, 和学分制对应
                syllabus 课表的JSON数据
        :return:
        """
        self.POST_PARSER.add_argument("username", required=True, location="form")
        self.POST_PARSER.add_argument("token", required=True, location="form")
        self.POST_PARSER.add_argument("start_year", type=int, required=True, location="form")
        self.POST_PARSER.add_argument("season", type=int, required=True, location="form")
        self.POST_PARSER.add_argument("collection_id", required=True, location="form")
        self.POST_PARSER.add_argument("syllabus", required=True, location="form")

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

        collector = common.query_single_by_filed(models.Collector, "collection_id", args["collection_id"])
        if collector is None:
            # 表明用户输入了错误的collection_id
            return {"error": "wrong collection_id"}, 404

        # 检查学期是否正确
        if collector.start_year != args["start_year"] or collector.season != args["season"]:
            return {"error": "semester doesn't match"}, 400

        collection = models.SyllabusCollection.query.filter_by(account=user.account).filter_by(collection_id=args["collection_id"]).first()

        if collection is not None:
            try:
                # 删除原有的数据
                print("deleting original data")
                db.session.delete(collection)
                db.session.commit()
            except Exception as e:
                return {"error": repr(e)}, 500

        collection = models.SyllabusCollection(collection_id=args["collection_id"], syllabus=args["syllabus"], account=args["username"])

        result = common.add_to_db(db, collection)
        if result == True:
            return {"id": collection.id}
        else:
            return {"error": "commit error in mysql"}, 500