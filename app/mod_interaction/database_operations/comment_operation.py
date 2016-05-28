# coding=utf-8
__author__ = 'smallfly'

from app.mod_interaction.models import Comment, UnRead, Post
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
    post = Post.query.with_entities(Post.uid).filter_by(id=post_id).first()
    if post is None:
        return False
    # 如果不是作者本人发表的这次评论, 那么通知作者
    if post.uid != comment_user_id:
        print("notifying author")
        db.session.add(UnRead(uid=post.uid, post_id=post_id))

    # 通知其他评论用户
    for comment in comments:
        # 不通知发表这次评论的人, 注意不要重复发送通知
        if comment.uid != comment_user_id and comment.uid != post.uid:
            unread = UnRead(uid=comment.uid, post_id=post_id)
            print('add unread for user', comment.uid)
            print('the unread:', repr(unread))
            db.session.add(unread)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("add unread error:", repr(e))
        db.session.rollback()
        return False

