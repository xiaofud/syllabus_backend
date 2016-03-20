# coding=utf-8
__author__ = 'smallfly'

# 对user model进行各类操作

from app.mod_interaction.database_operations import common
from app.mod_interaction.models import User
from app import db

def get_user_by_id(id):
    user = common.query_by_id(User, id)
    if user is None:
        print("user of id {} is None".format(id))
    return common.query_by_id(User, id)


def update_user_by_id(id, **kwargs):
    return common.update_model_by_id(User, db, id, **kwargs)