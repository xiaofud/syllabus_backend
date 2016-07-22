# coding=utf-8
__author__ = 'smallfly'

from app.mod_interaction import PostResource
from app.mod_interaction.database_operations import common
from app.mod_interaction import models
from app import db
from flask_restful.reqparse import RequestParser
from flask_restful import Resource

class ActivityResource(Resource):
    """
    校园活动即post_type=2的POST, 只有指定用户可以发布推文
    """

    def __init__(self):
        super(ActivityResource, self).__init__()

        # ------------------ GET ------------------
        self.get_parser = RequestParser(trim=True)
        self.get_parser.add_argument("")
        # ------------------ GET ------------------

        # ------------------ POST ------------------
        self.post_parser = RequestParser(trim=True)
        self.post_parser.add_argument("source", location="json")
        self.post_parser.add_argument("content", required=True, location="json")
        self.post_parser.add_argument("uid", type=int, required=True, location="json")
        self.post_parser.add_argument("token", required=True, location="json")
        # 这里可以不用管post_type参数, 保留同之前API兼容, 提高复用
        self.post_parser.add_argument("post_type", type=int, required=True, location="json")
        self.post_parser.add_argument("description", location="json")
        self.post_parser.add_argument("photo_list_json", location="json")
        # ------------------ POST ------------------

    def query(self, **kwargs):
        pass

    def get(self):
        pass

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        args["post_type"] = PostResource.Post.POST_TYPE_SCHOOL_ACTIVITY

        # 检查token
        if not common.check_token(args):
            return {"error": "wrong token"}, 401
        del args["token"]

        # 检测是否有权限发布
        super_users = models.User.query.with_entities(models.User.id).filter(models.User.level >= models.User.LEVEL_CAN_POST_ACTIVITY).all()
        super_ids = [user.id for user in super_users]
        if args["uid"] not in super_ids:
            return {"error": "HAVE NOT THE PRIORITY"}, 403  # 没有权限发布
        # 参数新的数据到数据库
        record_id = common.new_record(db, models.Post, **args)

        if record_id != False:
            return {"id": record_id}, 201  # crated
        else:
            return {"error": "failed"}, 500 # Internal Server Error

