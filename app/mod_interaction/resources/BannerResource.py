# coding=utf-8
__author__ = 'smallfly'

# 发布新的banner广告
from flask_restful import Resource
from app.mod_interaction.resources import helpers

class BannerResource(Resource):
    """
    返回最新的通知数据
    """
    def get(self):
        obj = helpers.get_notification()
        if obj is not None:
            return dict(latest=obj)
        else:
            return dict(ERROR="no resource"), 404

