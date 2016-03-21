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

    # 额外的处理
    EXTRA_CALLBACKS_FOR_METHODS_DICT = "EXTRA_CALLBACKS_FOR_METHODS_DICT"


    # 检测token
    TOKEN_CHECK_FOR_METHODS_DICT = "TOKEN_CHECK_FOR_METHODS_DICT"


    def __init__(self, **kwargs):
        self.accepted_variable_dict = kwargs[GenericResource.ACCEPTED_VARIABLE_DICT]
        self.model = kwargs[GenericResource.MODEL]
        self.resource_name = kwargs[GenericResource.RESOURCE_NAME]
        self.marshal_structure = kwargs[GenericResource.MARSHAL_STRUCTURE]
        self.parsers = kwargs[GenericResource.PARSERS_FOR_METHOD]
        self.time_to_string_list = kwargs.pop(GenericResource.TIMESTAMP_TO_STRING_LIST, None)
        self.not_allowed_methods = kwargs.pop(GenericResource.NOT_ALLOWED_METHODS_LIST, None)
        self.extra_callbacks = kwargs.pop(GenericResource.EXTRA_CALLBACKS_FOR_METHODS_DICT, None)
        self.token_check_callbacks = kwargs.pop(GenericResource.TOKEN_CHECK_FOR_METHODS_DICT, None)


    def get(self, id=None):

        # 先检查方法是否可用
        if self.not_allowed_methods is not None and "get" in self.not_allowed_methods:
            return {"error": "method not allowed"}, 403

        if id is None:
            return {"error": "bad request"}, 401

        if "get" in self.parsers:
            args = self.parsers["get"].parse_args()
            if "get" in self.accepted_variable_dict:
                helpers.clean_arguments(args, self.accepted_variable_dict["get"])
            # 进行时间处理
            if self.time_to_string_list is not None:
                for key in self.time_to_string_list:
                    if key in args:
                        args[key] = helpers.timestamp_to_string(args[key])

        # 看看是否需要检查token
        if self.token_check_callbacks is not None and "get" in self.token_check_callbacks:
            if not self.token_check_callbacks["get"](args):
                return {"error": "unauthorized"}, 401 # Unauthorized

        # 到这里要去掉token, 因为不允许用户写入token
        args.pop("token")

        thing = common.query_by_id(self.model, id)
        # 没找到的话
        if thing is None:
            return {"error": "invalid id {} for {}".format(id, self.resource_name)}, 404
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

        # 看看是否需要检查token
        if self.token_check_callbacks is not None and "post" in self.token_check_callbacks:
            if not self.token_check_callbacks["post"](args):
                return {"error": "unauthorized"}, 401 # Unauthorized

        # 到这里要去掉token, 因为不允许用户写入token
        args.pop("token")

        # 调用回调方法
        if self.extra_callbacks is not None and "post" in self.extra_callbacks:
            # print("callback")
            ret_val = self.extra_callbacks["post"](args)
            # 比如说有用户打算重复投票
            # print("called back returned")
            # print(args)
            if ret_val != False:
                return ret_val


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
            if "put" in self.accepted_variable_dict:
                helpers.clean_arguments(args, self.accepted_variable_dict["put"])
            # 进行时间处理
            if self.time_to_string_list is not None:
                for key in self.time_to_string_list:
                    if key in args:
                        args[key] = helpers.timestamp_to_string(args[key])

        # 看看是否需要检查token
        if self.token_check_callbacks is not None and "put" in self.token_check_callbacks:
            if not self.token_check_callbacks["put"](args):
                return {"error": "unauthorized"}, 401 # Unauthorized

        # 因为不允许更新id
        id = args.pop("id")

        # 到这里要去掉token, 因为不允许用户写入token
        args.pop("token")

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

        if "delete" in self.parsers:
            args = self.parsers["delete"].parse_args()
            if "delete" in self.accepted_variable_dict:
                helpers.clean_arguments(args, self.accepted_variable_dict["delete"])
            # 进行时间处理
            if self.time_to_string_list is not None:
                for key in self.time_to_string_list:
                    if key in args:
                        args[key] = helpers.timestamp_to_string(args[key])

        # 看看是否需要检查token
        if self.token_check_callbacks is not None and "delete" in self.token_check_callbacks:
            if not self.token_check_callbacks["delete"](args):
                return {"error": "unauthorized"}, 401 # Unauthorized

        result = common.delete_from_db(db, self.model, id)
        if result == True:
            return {"status": "deleted"}, 200
        else:
            if result[1] == common.ERROR_NOT_FOUND:
                return {"error": "{} not found".format(self.resource_name)}, 404
            else:
                return {"error": "failed"}, 500 # Internal Server Error
