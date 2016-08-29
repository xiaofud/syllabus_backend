# coding=utf-8
__author__ = 'smallfly'

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import db
from app.mod_interaction import models

class UserModelView(ModelView):

    column_searchable_list = ['nickname', 'account', 'id']

    column_list = ('id', "account", "visibility", 'level', 'image', "token")

    column_labels = {
        "id": "用户UID",
        "account": "账号名",
        "visibility": "删除标记(1未删除 2删除)",
        "level": "用户等级(0普通 1可以发布活动 2管理员)",
        "image": "头像",
        "token": "验证令牌"
    }

    column_editable_list = ("visibility", 'level', 'image', "token")

    page_size = 50

class PostModelView(ModelView):

    column_list = ('id',
                   "uid",
                   "post_type",
                   "description",
                   "content",
                   "post_time",
                   "visibility",
                   "source",
                   "photo_list_json",
                   "activity_start_time",
                   "activity_end_time",
                   "activity_location",
    )

    column_searchable_list = ("id", "uid", "description", "content", "source")

    column_labels = {
        "id": "序号",
        "uid": "发布用户ID",
        "post_type": "类型 0 普通文字信息 2 校园活动",
        "description": "描述",
        "content": "内容或者URL",
        "post_time": "发布时间",
        "visibility": "删除标记(1未删除 2删除)",
        "source": "来自",
        "photo_list_json": "图片列表",
        "activity_start_time": "活动开始时间",
        "activity_end_time": "活动结束时间",
        "activity_location": "活动地点"
    }

    page_size = 50

admin = Admin(name="课程后台管理", template_mode='bootstrap3')
admin.add_view(UserModelView(models.User, db.session, "用户管理"))
admin.add_view(PostModelView(models.Post, db.session, "动态管理"))
