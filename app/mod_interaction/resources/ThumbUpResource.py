# coding=utf-8
__author__ = 'smallfly'

from flask_restful import reqparse, fields
from app.mod_interaction.resources.GenericResource import GenericResource
from app.mod_interaction.models import ThumbUp
from app.mod_interaction.database_operations import thumb_up_operation

structure = {
    "id": fields.Integer,
    "post_time": fields.String,
    "post_id": fields.Integer,
    "uid": fields.Integer
}

post_parser = reqparse.RequestParser(trim=True)
post_parser.add_argument("post_id", required=True, type=int, location="json")
post_parser.add_argument("uid", required=True, type=int, location="json")


INITIAL_KWARGS = {
    GenericResource.ACCEPTED_VARIABLE_DICT: {
        "post": ["post_id", "uid", "comment"],
    },
    GenericResource.MARSHAL_STRUCTURE: structure,
    GenericResource.MODEL:ThumbUp,
    GenericResource.RESOURCE_NAME: "like",
    GenericResource.PARSERS_FOR_METHOD:{
        "post": post_parser,
    },
    GenericResource.NOT_ALLOWED_METHODS_LIST:[
        "put"
    ],
    GenericResource.EXTRA_CALLBACKS_FOR_METHODS_DICT:{
        "post": thumb_up_operation.check_multiple_likes
    }
}

