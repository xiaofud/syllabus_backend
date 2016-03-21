# coding=utf-8
__author__ = 'smallfly'

from app.mod_interaction.database_operations import common
from app.mod_interaction.database_operations import user_operation
from app.mod_interaction.models import Post
from app import db

def get_post_by_id(id):
    post = common.query_by_id(Post, id)
    if post is None:
        print("post of id {} is None".format(id))
    return common.query_by_id(Post, id)


def update_post_by_id(id, **kwargs):
    return common.update_model_by_id(Post, db, id, **kwargs)

def new_post(**kwargs):
    return common.new_record(db, Post, **kwargs)

def check_token(args):
    uid = args.get("uid")
    token = args.get("token")
    if uid is None or token is None:
        return False
    if uid is not None and token is not None:
        user = user_operation.get_user_by_id(uid)
        if user is None:
            return False
        print("token for {} is {}".format(user.account, user.token))
        if user.token == token:
            return True
    return False
