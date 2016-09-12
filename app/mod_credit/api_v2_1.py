# coding=utf-8
__author__ = 'smallfly'

# coding=utf-8
__author__ = 'smallfly'

# 用于和内网的学分制系统交互的模块

from flask import Blueprint, make_response
from app.mod_credit.resources.class_member_resource import ClassMember
from app.mod_credit.resources.syllabus_resource import SyllabusResource
from app.mod_credit.resources.exam_resource import ExamResource
from app.mod_credit.resources.grade_resource import GradeResource
from app.mod_credit.resources.oa_resource import OAResource
from app.mod_credit.resources.wechat_auth_resource import WechatAuthResource
from app.mod_interaction.resources import ResultResponse
from flask_restful import Api

credit_blueprint2_1 = Blueprint("credit_blueprint2", __name__, url_prefix="/credit")

api_v2_1 = Api(credit_blueprint2_1, prefix="/api/v2.1")

# http://flask-restful-cn.readthedocs.io/en/0.3.5/extending.html
@api_v2_1.representation("application/json")
def output_json(data, code, headers=None):
    response_data = ResultResponse.ResultResponse()
    response_data.code = code
    # response_data.data = data
    if "error" in data:
        response_data.message = data["error"]
        response_data.data = {}
    elif "ERROR" in data:
        response_data.message = data["ERROR"]
        response_data.data = {}
    else:
        response_data.data = data
        if 200 < code or code > 200:
            response_data.message = 'fail'
        else:
            response_data.message = 'ok'
    resp = make_response(response_data.to_json(), code)
    resp.headers.extend(headers or {})
    return resp

api_v2_1.add_resource(ClassMember, "/member", "/member/", endpoint="member")
api_v2_1.add_resource(SyllabusResource, "/syllabus", "/syllabus/", endpoint="syllabus")

# curl localhost:8080/credit/api/v2/exam -X POST -d "username=14xfdeng&password=*****&years=2015-2016&semester=1"
api_v2_1.add_resource(ExamResource, "/exam", "/exam/", endpoint="exam")

api_v2_1.add_resource(GradeResource, "/grade", "/grade/", endpoint="grade")

api_v2_1.add_resource(OAResource, "/oa", "/oa/", endpoint="oa")

api_v2_1.add_resource(WechatAuthResource, "/auth", "/auth/", endpoint="auth")
