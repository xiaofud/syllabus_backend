# coding=utf-8
__author__ = 'smallfly'

# 用于和内网的学分制系统交互的模块

from flask import Blueprint
from app.mod_credit.resources.class_member_resource import ClassMember
from flask_restful import Api

credit_blueprint = Blueprint("credit_blueprint", __name__, url_prefix="/credit")

api = Api(credit_blueprint, prefix="/api/v2")

api.add_resource(ClassMember, "/member", "/member/", endpoint="member")

