# coding=utf-8
__author__ = 'smallfly'

from app.mod_interaction.models import Comment, UnRead
from app import db

def new_unread(post_id, comment_user_id):
    """
    添加新的未读信息
    除了comment_user_id这个用户外, 其他参与到了该post的用户都会
    加入未读列表
    :param post_id: post id
    :param comment_user_id: 当前评价的人
    :return:
    """

    # 找到所有先前评论过 post_id 所指向的post
    # return model.query.with_entities(model.id).order_by(model.id.desc()).first().id
    comments = Comment.query.with_entities(Comment.uid).filter_by(post_id=post_id).all()

    for comment in comments:
        if comment.uid != comment_user_id:
            unread = UnRead(uid=comment.uid, post_id=post_id)
            db.session.add(unread)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("add unread error:", repr(e))
        db.session.rollback()
        return False

