# coding=utf-8
__author__ = 'smallfly'

from app.mod_interaction.models import ThumbUp
from app.mod_interaction.database_operations import common

def has_liked(uid, pid):
    """
    检查uid这位用户是否已经给pid这篇post点过赞了
    :param uid: 用户
    :param pid: post
    :return:
    """
    all_likes = common.fetch_all(ThumbUp)
    if len(all_likes) == 0:
        # print("empty")
        return False
    else:
        # 检查该用户是否点过赞了
        for like in all_likes:
            if like.uid == uid and pid == like.post_id:
                return True
    return False

def check_multiple_likes(args):
    uid = args.get("uid")
    pid = args.get("post_id")
    # print("uid", uid, "pid", pid)
    if has_liked(uid, pid):
        return {"error": "can't like the same post more than once"}, 403    # FORBIDDEN
    else:
        return False
