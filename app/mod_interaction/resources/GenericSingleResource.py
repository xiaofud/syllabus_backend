# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, marshal
from app.mod_interaction.database_operations import common
from app.mod_interaction.resources import helpers
from app import db

class GenericSingleResource(Resource):
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

    # 获取数据的函数
    # 接口声明
    # def get_resource(model, id, **kwargs):
    #     pass
    RESOURCE_GETTER = "RESOURCE_GETTER"



    def __init__(self, **kwargs):
        self.accepted_variable_dict = kwargs[GenericSingleResource.ACCEPTED_VARIABLE_DICT]
        self.model = kwargs[GenericSingleResource.MODEL]
        self.resource_name = kwargs[GenericSingleResource.RESOURCE_NAME]
        self.marshal_structure = kwargs[GenericSingleResource.MARSHAL_STRUCTURE]
        self.parsers = kwargs[GenericSingleResource.PARSERS_FOR_METHOD]
        self.time_to_string_list = kwargs.pop(GenericSingleResource.TIMESTAMP_TO_STRING_LIST, None)
        self.not_allowed_methods = kwargs.pop(GenericSingleResource.NOT_ALLOWED_METHODS_LIST, None)
        self.extra_callbacks = kwargs.pop(GenericSingleResource.EXTRA_CALLBACKS_FOR_METHODS_DICT, None)
        self.token_check_callbacks = kwargs.pop(GenericSingleResource.TOKEN_CHECK_FOR_METHODS_DICT, None)
        self.resource_getter = kwargs.pop(GenericSingleResource.RESOURCE_GETTER, None)


    def get(self, id=None):

        # 先检查方法是否可用
        if self.not_allowed_methods is not None and "get" in self.not_allowed_methods:
            return {"error": "method not allowed"}, 405

        if id is None:
            return {"error": "bad request"}, 400

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
                else:
                    # 到这里要去掉token, 因为不允许用户写入token
                    args.pop("token")


        thing = common.query_single_by_id(self.model, id)
        if thing is None:
            return {"error": "invalid id {} for {}".format(id, self.resource_name)}, 404
        return marshal(thing, self.marshal_structure), 200

    def post(self):

        # 先检查方法是否可用
        if self.not_allowed_methods is not None and "post" in self.not_allowed_methods:
            return {"error": "method not allowed"}, 405



        if "post" in self.parsers:
            args = self.parsers["post"].parse_args()
            # print(args)
            if "post" in self.accepted_variable_dict:
                helpers.clean_arguments(args, self.accepted_variable_dict["post"])
            # 进行时间处理
            if self.time_to_string_list is not None:
                for key in self.time_to_string_list:
                    if key in args:
                        args[key] = helpers.timestamp_to_string(args[key])

            # 看看是否需要检查token
            if self.token_check_callbacks is not None and "post" in self.token_check_callbacks:
                print("token checking")
                # print("checking token")
                # print("input token", args["token"])
                if not self.token_check_callbacks["post"](args):
                    return {"error": "unauthorized"}, 401 # Unauthorized

            # 到这里要去掉token, 因为不允许用户写入token
            args.pop("token")

        # 调用回调方法
        if self.extra_callbacks is not None and "post" in self.extra_callbacks:
            print("callback")
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
            return {"error": "method not allowed"}, 405

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
                # print("need to check token")
                if not self.token_check_callbacks["put"](args):
                    # print(args["uid"], args["id"], args["token"])
                    return {"error": "unauthorized"}, 401 # Unauthorized

            # 因为不允许更新id
            id = args.pop("id")

            # 到这里要去掉token, 因为不允许用户写入token
            args.pop("token")

        # result = post_operation.update_post_by_id(id, **args)
        uid = args.pop("uid")
        result = common.update_model_by_id(self.model, db, id, uid, **args)
        if result == True:
            return {"status": "updated"}, 200
        else:
            if result[1] == common.ERROR_NOT_FOUND:
                return {"error": "{} not found".format(self.resource_name)}, 404
            elif result[1] == common.ERROR_COMMIT_FAILED:
                return {"error": "failed"}, 500 # Internal Server Error
            elif result[1] == common.ERROR_USER_ID_CONFLICT:
                return {"error": "kidding me?"}, 401

    def delete(self, id=None):

        # 先检查方法是否可用
        if self.not_allowed_methods is not None and "delete" in self.not_allowed_methods:
            return {"error": "method not allowed"}, 405

        # if id is None:
        #     return {"error": "bad request"}, 401

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

            result = common.delete_from_db(db, self.model, args["id"], args["uid"])
            if result == True:
                return {"status": "deleted"}, 200
            else:
                if result[1] == common.ERROR_NOT_FOUND:
                    return {"error": "{} not found".format(self.resource_name)}, 404
                elif result[1] == common.ERROR_COMMIT_FAILED:
                    return {"error": "failed"}, 500 # Internal Server Error
                elif result[1] == common.ERROR_USER_ID_CONFLICT:
                    return {"error": "kidding me?"}, 403
        return {"error": "bad request"}, 400
