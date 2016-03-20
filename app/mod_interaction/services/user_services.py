# coding=utf-8
__author__ = 'smallfly'

# 对user model进行各类操作

from app.mod_interaction.services import common
from app.mod_interaction.models import User

def get_user_by_id(id):
    return common.query_by_id(User, id)