# coding=utf-8
__author__ = 'smallfly'

from app import db
from app.mod_interaction import PostResource
from app.mod_interaction.database_operations import common
from app.mod_interaction import models
from app.mod_interaction.resources import helpers
from flask_restful.reqparse import RequestParser
from flask_restful import Resource, fields, marshal

import time

ACTIVITY_STRUCTURE = {
    "id": fields.Integer,
    "post_type": fields.Integer,
    # "title": fields.String,
    "content": fields.String,
    "post_time": fields.String,
    "source":fields.String,
    "user": fields.Nested(PostResource.user_structure),
    "description": fields.String,
    "thumb_ups": fields.List(fields.Nested(PostResource.thumb_ups_structure)),
    "comments": fields.List(fields.Nested(PostResource.comment_structure)),
    "photo_list_json": fields.String,

    "activity_start_time": fields.String,
    "activity_end_time": fields.String,
    "activity_location": fields.String
}

class ActivityResource(Resource):
    """
    校园活动即post_type=2的POST, 只有指定用户可以发布推文
    """

    def __init__(self):
        super(ActivityResource, self).__init__()

        # ------------------ GET ------------------
        """
        请求地址: /interaction/api/v2/activity
        请求方法: GET
        参数:
            可选参数:
                type 整型值,
                    0(默认值) 表示结果按照活动开始时间排序返回
                    1 表示结果按照发布时间排序返回
                activity_start_time 时间戳
                    type 为 0 时才有意义
                    表示服务器根据activity_start_time为界限,
                    比如activity_start_time为 2016/8/16 那么返回的活动将会是
                    那些已经开始了但是开始时间晚于或者等于2016/8/16的活动
                    以及未来的并未开始的活动
                page_index 页码
                page_size 每页的结果数
        """
        self.get_parser = RequestParser(trim=True)
        self.get_parser.add_argument("type", type=int, location="args")
        self.get_parser.add_argument("timestamp", type=int, location="args")
        # 用于分页
        self.get_parser.add_argument("page_index", type=int, location="args")
        # 用于分页
        self.get_parser.add_argument("page_size", type=int, location="args")


        # ------------------ GET ------------------

        # ------------------ POST ------------------
        """
        请求地址: /interaction/api/v2/activity
        请求方法: POST
        参数: 以json方式传递参数
            必须参数:
                source 来源, iOS Android 或者可以是部门
                content 此处作为活动的URL
                uid 发布用户的id, 如果用户无权限发布, 那么会返回 403
                token 用户的token
                post_type 取 2
                activity_start_time 活动起始时间戳
                activity_end_time 活动结束时间戳
            可选参数:
                activity_location 活动地点, 如果未指定, 那么默认为 未指定
                description 活动描述
                photo_list_json 同Post的图片格式
        """
        self.post_parser = RequestParser(trim=True)
        self.post_parser.add_argument("source", location="json")
        self.post_parser.add_argument("content", required=True, location="json")
        self.post_parser.add_argument("uid", type=int, required=True, location="json")
        self.post_parser.add_argument("token", required=True, location="json")
        # 这里可以不用管post_type参数, 保留同之前API兼容, 提高复用
        self.post_parser.add_argument("post_type", type=int, required=True, location="json")
        self.post_parser.add_argument("activity_start_time", type=int, required=True, location="json")
        self.post_parser.add_argument("activity_end_time", type=int, required=True, location="json")


        self.post_parser.add_argument("activity_location", required=False, location="json")
        self.post_parser.add_argument("description", location="json")
        self.post_parser.add_argument("photo_list_json", location="json")
        # ------------------ POST ------------------

    def query(self, arg_dict):
        # 分页 http://my.oschina.net/ranvane/blog/196906

        # 读取条件

        # 读取类型
        # 默认值为0
        type_ = arg_dict["type"] or 0

        # 设置时间条件
        now = helpers.timestamp_to_string(int(time.time()))
        start_time = arg_dict["activity_start_time"] or now

        # print(depart_time)

        page_index = arg_dict["page_index"] or 1

        page_size = arg_dict["page_size"] or 10

        if type_ == 0:
            # 按照活动开始时间排序
            page_obj = \
                models.Post.query\
                    .filter(models.Post.post_type == models.Post.POST_TYPE_SCHOOL_ACTIVITY)\
                    .filter(models.Post.activity_start_time >= start_time)\
                    .order_by(models.Post.activity_start_time.asc())\
                    .paginate(page_index, page_size, False)
        else:
            # 按照发布时间排序
            page_obj = \
                models.Post.query\
                    .filter(models.Post.post_type == models.Post.POST_TYPE_SCHOOL_ACTIVITY)\
                    .order_by(models.Post.id.desc())\
                    .paginate(page_index, page_size, False)

        activities = page_obj.items


        return activities

    def get(self):
        args = self.get_parser.parse_args(strict=True)

        activities = self.query(args)

        if len(activities) > 0:
            return marshal(activities, ACTIVITY_STRUCTURE)
        else:
            return {"error": "nothing found"}, 404

    def post(self):
        args = self.post_parser.parse_args(strict=True)
        args["post_type"] = PostResource.Post.POST_TYPE_SCHOOL_ACTIVITY

        # 检查token
        if not common.check_token(args):
            return {"error": "wrong token"}, 401
        del args["token"]

        args["activity_location"] = args["activity_location"] or "未指定"

        # 处理时间
        for key in ("activity_start_time", "activity_end_time"):
            args[key] = helpers.timestamp_to_string(args[key])


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

