# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, marshal
from app.mod_interaction.database_operations import common

class GenericMultipleResource(Resource):
    """
    主要用于get多份数据
    """

    # 数据的展示结构
    MARSHAL_STRUCTURE = "MARSHAL_STRUCTURE"

    # 数据模型
    MODEL = "MODEL"

    # 参数解析器
    PARSER_FOR_METHODS_DICT = "PARSER_FOR_METHODS_DICT"

    # 用于封装最后的结果, 即 {"ENVELOPE": result}
    ENVELOPE = "ENVELOPE"

    def __init__(self, **kwargs):
        self.marshal_structure = kwargs.pop(GenericMultipleResource.MARSHAL_STRUCTURE, None)
        self.model = kwargs.pop(GenericMultipleResource.MODEL, None)
        self.parsers = kwargs.pop(GenericMultipleResource.PARSER_FOR_METHODS_DICT, None)
        self.envelope = kwargs.pop(GenericMultipleResource.ENVELOPE, "data_list")


    def get(self):
        args = {}
        if "get" in self.parsers:
            args.update(self.parsers["get"].parse_args())
        result = common.query_multiple(self.model, **args)
        # print(result)
        if len(result) == 0:
            return {"error": "no resources yet"}, 401
        else:
            return marshal(result, self.marshal_structure, envelope=self.envelope)

