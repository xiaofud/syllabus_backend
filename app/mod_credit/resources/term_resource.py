# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource
from app.mod_interaction.resources import helpers

class TermResource(Resource):

    def get(self):
        term = helpers.get_term()
        if term is None:
            return {"error": "no information found."}, 404
        return term