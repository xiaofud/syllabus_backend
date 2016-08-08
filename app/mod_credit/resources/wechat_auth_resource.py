# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.mod_interaction.database_operations import common
from app.mod_interaction import models
import requests

WECHAT_AUTH_API = "http://wechat.stu.edu.cn/wechat/login/login_verify"
CODE_FALSE = 1
CODE_INTERNET_ERROR = 2
CODE_OKAY = 0

class WechatAuthResource(Resource):

    def __init__(self):
        super(WechatAuthResource, self).__init__()
        self.get_parser = RequestParser(trim=True)
        self.get_parser.add_argument("username", required=True, location="form")
        self.get_parser.add_argument("password", required=True, location="form")

    def post(self):
        args = self.get_parser.parse_args(strict=True)
        status = auth(args["username"], args["password"])
        if status["code"] == CODE_OKAY:
            user = common.query_single_by_filed(models.User, "account", args["username"])
            if user is None:
                return {"error": "account correct but not found in database"}, 404
            return {"token": user.token}, 200
        elif status["code"] == CODE_FALSE:
            # 凭证有误
            return {"error": "incorrect"}, 401
        else:
            # 内部网络错误
            return {"error": "INTERNET FAILURE"}, 500


def auth(username, password):
    """
    使用微信方式验证
    :param username:    帐号名
    :param password:    密码
    :return:    True, 账号密码匹配 False 账号密码不匹配 None 网络错误
    """
    post_data = {
        "ldap_account": username,
        "ldap_password": password,
        "btn_ok": "登录",
        "source_type": "",
        "openid": ""
    }
    status = {
        "code": CODE_OKAY,
        "message": "OKAY"
    }
    try:
        resp = requests.post(WECHAT_AUTH_API, data=post_data)
        if resp.ok:
            if "账号或者密码错误" in resp.text:
                status["code"] = CODE_FALSE
                status["message"] = "incorrect account or password"
                return status
            else:
                return status
    except requests.RequestException as e:
        print(e)
        status["code"] = CODE_INTERNET_ERROR
        status["message"] = "INTERNET FAILED"
        return status

if __name__ == "__main__":
    status = auth("14xfdeng", "")
    print(status)
