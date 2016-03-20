# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, fields, marshal, reqparse
from app.mod_interaction.services import user_services


structure = {
    "id": fields.Integer,
    "account": fields.String,
    "nickname": fields.String,
    "gender": fields.Integer,
    "birthday": fields.String,
    "profile": fields.String
}


class User(Resource):

    # curl localhost:8080/interaction/api/v2/user/1 -i
    def get(self, id):
        user = user_services.get_user_by_id(id)
        if user is None:
            data = {
                "error": "invalid id"
            }
            return data, 404    # not found
        return marshal(user, structure), 200

