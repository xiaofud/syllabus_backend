# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, reqparse
import requests
import requests.exceptions

get_parser = reqparse.RequestParser(trim=True)
get_parser.add_argument("class_id", type=int, required=True, location="args")

class ClassMember(Resource):

    def get(self):
        args = get_parser.parse_args()

        params = {
            "class_id": args["class_id"]
        }
        try:
            resp = requests.get("http://121.42.175.83:8084/api/v1.0/member", params=params)
            return resp.json()
        except requests.exceptions.ConnectionError:
            return {"error": "connection refused"}, 400
