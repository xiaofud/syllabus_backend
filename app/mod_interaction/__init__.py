# coding=utf-8
__author__ = 'smallfly'

# 存放了用户数据, 以及活动之类的互动.

from flask import Blueprint
interaction_blueprint = Blueprint("interaction", __name__, url_prefix="/interaction")   # url 必须以 / 开头

# 加载数据表
from app.mod_interaction import models

# 加载Resource
from app.mod_interaction.resources.User import User

from flask_restful import Api

api = Api(interaction_blueprint, prefix="/api/v2")

# curl localhost:8080/interaction/api/v2/user/1
api.add_resource(User, "/user/<int:id>", endpoint="user")





