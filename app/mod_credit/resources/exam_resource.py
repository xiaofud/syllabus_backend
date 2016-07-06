# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, reqparse

import requests
import requests.exceptions

parser = reqparse.RequestParser(trim=True)

parser.add_argument("username", required=True, location="form")
parser.add_argument("password", required=True, location="form")
parser.add_argument("years", required=True, location="form")
parser.add_argument("semester", required=True, location="form")

class ExamResource(Resource):

    def post(self):
        args = parser.parse_args()
        try:
            resp = requests.post("http://127.0.0.1:8084/exam", data=args)
            return resp.json()
        except requests.exceptions.ConnectionError:
            return {"error": "connection refused"}, 400
