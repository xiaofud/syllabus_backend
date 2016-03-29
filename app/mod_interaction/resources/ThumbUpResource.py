# coding=utf-8
__author__ = 'smallfly'

from flask_restful import reqparse, fields
from app.mod_interaction.resources.GenericSingleResource import GenericSingleResource
from app.mod_interaction.models import ThumbUp
from app.mod_interaction.database_operations import thumb_up_operation, common


SINGLE_THUMB_UP_STRUCTURE = {
    "id": fields.Integer,
    "post_time": fields.String,
    "post_id": fields.Integer,
    "uid": fields.Integer
}

post_parser = reqparse.RequestParser(trim=True)
post_parser.add_argument("post_id", required=True, type=int, location="json")
post_parser.add_argument("uid", required=True, type=int, location="json")
post_parser.add_argument("token", required=True, location="json")

delete_parser = reqparse.RequestParser(trim=True)
delete_parser.add_argument("id", required=True, type=int, location="headers")
delete_parser.add_argument("uid", required=True, type=int, location="headers")
delete_parser.add_argument("token", required=True, location="headers")



SINGLE_THUMB_UP_INITIAL_KWARGS = {
    GenericSingleResource.ACCEPTED_VARIABLE_DICT: {
        "post": ["post_id", "uid", "comment", "token"],
    },
    GenericSingleResource.MARSHAL_STRUCTURE: SINGLE_THUMB_UP_STRUCTURE,
    GenericSingleResource.MODEL:ThumbUp,
    GenericSingleResource.RESOURCE_NAME: "like",
    GenericSingleResource.PARSERS_FOR_METHOD:{
        "post": post_parser,
        "delete": delete_parser
    },
    GenericSingleResource.NOT_ALLOWED_METHODS_LIST:[
        "put"
    ],
    GenericSingleResource.EXTRA_CALLBACKS_FOR_METHODS_DICT:{
        "post": thumb_up_operation.check_multiple_likes
    },
    GenericSingleResource.TOKEN_CHECK_FOR_METHODS_DICT:{
        "post": common.check_token,
        "delete": common.check_token
    }
}

