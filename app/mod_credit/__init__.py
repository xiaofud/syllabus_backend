# coding=utf-8
__author__ = 'smallfly'

# 用于和内网的学分制系统交互的模块

from flask import Blueprint
from app.mod_credit.resources.class_member_resource import ClassMember
from app.mod_credit.resources.syllabus_resource import SyllabusResource
from app.mod_credit.resources.exam_resource import ExamResource
from app.mod_credit.resources.grade_resource import GradeResource
from app.mod_credit.resources.oa_resource import OAResource
from app.mod_credit.resources.wechat_auth_resource import WechatAuthResource
from app.mod_credit.resources.oauth2_token_resource import OAUTH2TokenResource
from app.mod_credit.resources.oauth2_refresh_token_resource import OAUTH2RefreshTokenResource
from flask_restful import Api

credit_blueprint = Blueprint("credit_blueprint", __name__, url_prefix="/credit")

api = Api(credit_blueprint, prefix="/api/v2")

api.add_resource(ClassMember, "/member", "/member/", endpoint="member")
api.add_resource(SyllabusResource, "/syllabus", "/syllabus/", endpoint="syllabus")

# curl localhost:8080/credit/api/v2/exam -X POST -d "username=14xfdeng&password=*****&years=2015-2016&semester=1"
api.add_resource(ExamResource, "/exam", "/exam/", endpoint="exam")

api.add_resource(GradeResource, "/grade", "/grade/", endpoint="grade")

api.add_resource(OAResource, "/oa", "/oa/", endpoint="oa")

api.add_resource(WechatAuthResource, "/auth", "/auth/", endpoint="auth")

api.add_resource(OAUTH2TokenResource, "/token", "/token/", endpoint="token")

api.add_resource(OAUTH2RefreshTokenResource, "/refresh_token", "/refresh_token/", endpoint="refresh_token")