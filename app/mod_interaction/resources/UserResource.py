# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, fields, marshal, reqparse
from app.mod_interaction.database_operations import user_operation
from datetime import datetime

structure = {
    "id": fields.Integer,
    "account": fields.String,
    "nickname": fields.String,
    "gender": fields.Integer,
    "birthday": fields.String,
    "profile": fields.String
}

put_parser = reqparse.RequestParser(trim=True)
put_parser.add_argument("id", type=int, required=True, location='json')
# 后面需要token限制
put_parser.add_argument("nickname", location='json')
# 使用时间戳
put_parser.add_argument("birthday", type=int, location='json')
put_parser.add_argument("profile", location='json')
put_parser.add_argument("gender", location='json')


class UserResource(Resource):

    # 对外的接口仅仅允许修改这些数据
    ACCEPT_VARIABLES = ("id", "nickname", "birthday", "profile", "gender")

    # curl localhost:8080/interaction/api/v2/user/1 -i
    def get(self, id):
        user = user_operation.get_user_by_id(id)
        if user is None:
            return {"error": "invalid id"}, 404    # not found
        return marshal(user, structure), 200

    # curl --header "Content-type: application/json" localhost:8080/interaction/api/v2/user -X PUT -d '{"id": 1, "birthday": "819648000", "nickname": "xiaofud", "gender": 1, "profile": "hello world"}'
    # date -d "1995-12-23" "+%s"    获取时间戳
    def put(self):
        args = put_parser.parse_args()
        if args["birthday"] is not None:
            birthday = datetime.fromtimestamp(int(args["birthday"]))
            birthday = birthday.strftime("%Y-%m-%d %H:%M:%S")
            args["birthday"] = birthday
            # print(birthday)
        user_id = args.pop("id")
        # 去除其他参数, 避免用户自己修改token之类的数据
        for arg in args:
            if arg not in UserResource.ACCEPT_VARIABLES:
                args.pop(arg)
        result = user_operation.update_user_by_id(user_id, **args)
        if result == True:
            return {"status": "updated"}, 200
        else:
            if result[1] == user_operation.common.ERROR_NOT_FOUND:
                return {"error": "user not found"}, 404
            else:
                return {"error": "failed"}, 500 # Internal Server Error


# Argument Locations
# By default, the RequestParser tries to parse values from flask.Request.values, and flask.Request.json.
#
# Use the location argument to add_argument() to specify alternate locations to pull the values from. Any variable on the flask.Request can be used. For example:
#
# # Look only in the POST body
# parser.add_argument('name', type=int, location='form')
#
# # Look only in the querystring
# parser.add_argument('PageSize', type=int, location='args')
#
# # From the request headers
# parser.add_argument('User-Agent', location='headers')
#
# # From http cookies
# parser.add_argument('session_id', location='cookies')
#
# # From file uploads
# parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
# Note
# Only use type=list when location='json'. See this issue for more details