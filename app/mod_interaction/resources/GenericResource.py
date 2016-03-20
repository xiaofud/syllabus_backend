# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, marshal
from app.mod_interaction.database_operations import common
from app.mod_interaction.resources import helpers
from app import db

class GenericResource(Resource):
    """
    通用形的Resource
    """

    # 存放各种方法应该接受的参数
    ACCEPTED_VARIABLE_DICT = "ACCEPTED_VARIABLE_DICT"

    # 数据库model
    MODEL = "MODEL"

    # resource 的名称
    RESOURCE_NAME = "RESOURCE_NAME"

    # 展示数据的结构
    MARSHAL_STRUCTURE = "MARSHAL_STRUCTURE"

    # 各个方法的 request parser
    PARSERS_FOR_METHOD = "METHOD_PARSERS"

    # 转换时间, 需要从时间戳转换为字符串的参数列表
    TIMESTAMP_TO_STRING_LIST = "TIMESTAMP_TO_STRING_LIST"

    # 禁用的http方法
    NOT_ALLOWED_METHODS_LIST = "NOT_ALLOWED_METHODS_LIST"



    def __init__(self, **kwargs):
        self.accepted_variable_dict = kwargs[GenericResource.ACCEPTED_VARIABLE_DICT]
        self.model = kwargs[GenericResource.MODEL]
        self.resource_name = kwargs[GenericResource.RESOURCE_NAME]
        self.marshal_structure = kwargs[GenericResource.MARSHAL_STRUCTURE]
        self.parsers = kwargs[GenericResource.PARSERS_FOR_METHOD]
        self.time_to_string_list = kwargs.pop(GenericResource.TIMESTAMP_TO_STRING_LIST, None)
        self.not_allowed_methods = kwargs.pop(GenericResource.NOT_ALLOWED_METHODS_LIST, None)


    def get(self, id=None):

        # 先检查方法是否可用
        if self.not_allowed_methods is not None and "get" in self.not_allowed_methods:
            return {"error": "method not allowed"}, 403

        if id is None:
            return {"error": "bad request"}, 401
        thing = common.query_by_id(self.model, id)
        # 没找到的话
        if thing is None:
            return {"error": "invalid id{} for{}".format(id, self.resource_name)}, 404
        return marshal(thing, self.marshal_structure), 200

    def post(self):

        # 先检查方法是否可用
        if self.not_allowed_methods is not None and "post" in self.not_allowed_methods:
            return {"error": "method not allowed"}, 403

        if "post" in self.parsers:
            args = self.parsers["post"].parse_args()
            if "post" in self.accepted_variable_dict:
                helpers.clean_arguments(args, self.accepted_variable_dict["post"])
            # 进行时间处理
            if self.time_to_string_list is not None:
                for key in self.time_to_string_list:
                    if key in args:
                        args[key] = helpers.timestamp_to_string(args[key])

        result = common.new_record(db, self.model, **args)
        if result != False:
            return {"id": result}, 201  # crated
        else:
            return {"error": "failed"}, 500 # Internal Server Error

    def put(self):

        # 先检查方法是否可用
        if self.not_allowed_methods is not None and "put" in self.not_allowed_methods:
            return {"error": "method not allowed"}, 403

        if "put" in self.parsers:
            args = self.parsers["put"].parse_args()
            helpers.clean_arguments(args, self.accepted_variable_dict["put"])
            # 进行时间处理
            if self.time_to_string_list is not None:
                for key in self.time_to_string_list:
                    if key in args:
                        args[key] = helpers.timestamp_to_string(args[key])
        # 因为不允许更新id
        id = args.pop("id")
        # result = post_operation.update_post_by_id(id, **args)
        result = common.update_model_by_id(self.model, db, id, **args)
        if result == True:
            return {"status": "updated"}, 200
        else:
            if result[1] == common.ERROR_NOT_FOUND:
                return {"error": "{} not found".format(self.resource_name)}, 404
            else:
                return {"error": "failed"}, 500 # Internal Server Error

    def delete(self, id=None):

        # 先检查方法是否可用
        if self.not_allowed_methods is not None and "delete" in self.not_allowed_methods:
            return {"error": "method not allowed"}, 403

        if id is None:
            return {"error": "bad request"}, 401
        result = common.delete_from_db(db, self.model, id)
        if result == True:
            return {"status": "deleted"}, 200
        else:
            if result[1] == common.ERROR_NOT_FOUND:
                return {"error": "{} not found".format(self.resource_name)}, 404
            else:
                return {"error": "failed"}, 500 # Internal Server Error

