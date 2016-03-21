# coding=utf-8
__author__ = 'smallfly'

from flask_restful import reqparse, fields
from app.mod_interaction.resources.GenericResource import GenericResource
from app.mod_interaction.database_operations import common
from app.mod_interaction.models import Comment

structure = {
    "id": fields.Integer,
    "post_time": fields.String,
    "comment": fields.String,
    "post_id": fields.Integer,
    "uid": fields.Integer
}

post_parser = reqparse.RequestParser(trim=True)
post_parser.add_argument("post_id", required=True, type=int, location="json")
post_parser.add_argument("uid", required=True, type=int, location="json")
post_parser.add_argument("comment", required=True, location="json")
post_parser.add_argument("token", required=True, location="json")


put_parser = post_parser.copy()
put_parser.add_argument("id", required=True, type=int, location="json")

delete_parser = reqparse.RequestParser(trim=True)
delete_parser.add_argument("uid", required=True, type=int, location="json")
delete_parser.add_argument("token", required=True, location="json")
delete_parser.add_argument("id", required=True, type=int, location="json")

INITIAL_KWARGS = {
    GenericResource.ACCEPTED_VARIABLE_DICT: {
        "put": ["id", "post_id", "uid", "comment", "token"],
        "post": ["post_id", "uid", "comment", "token"],
    },
    GenericResource.MARSHAL_STRUCTURE: structure,
    GenericResource.MODEL:Comment,
    GenericResource.RESOURCE_NAME: "comment",
    GenericResource.PARSERS_FOR_METHOD:{
        "post": post_parser,
        "put": put_parser,
        "delete": delete_parser
    },
    GenericResource.TOKEN_CHECK_FOR_METHODS_DICT:{
        "post": common.check_token,
        "put": common.check_token,
        "delete": common.check_token
    }
}