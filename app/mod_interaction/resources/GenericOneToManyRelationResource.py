# coding=utf-8
__author__ = 'smallfly'

# 适用于:
# 查找某个Post的所有评论

from flask_restful import marshal
from app.mod_interaction.resources.GenericMultipleResource import GenericMultipleResource
from app.mod_interaction.database_operations import common

class GenericOneToManyRelationResource(GenericMultipleResource):

    def get(self):
        args = {}
        if "get" in self.parsers:
            args.update(self.parsers["get"].parse_args())
        result = common.query_one_to_many(self.model, **args)

        if result == False:
            return {"error": "wrong field name"}, 400

        if len(result) == 0:
            return {"error": "no resources yet"}, 404
        else:
            return marshal(result, self.marshal_structure, envelope=self.envelope)

