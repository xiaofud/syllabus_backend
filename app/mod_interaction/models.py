# coding=utf-8
__author__ = 'smallfly'

from app import db

SUPER_USERS = [
    "14xfdeng",
    "14jhwang",
    "13yjli3"
]

# 用户表
class User(db.Model):

    # 性别常量
    GENDER_FEMALE = 0
    GENDER_MALE = 1

    USER_NOT_FORBIDDEN = 1
    USER_FORBIDDEN = 0


    __tablename__ = "users" # 表名

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 用户账号
    account = db.Column(db.String(20), nullable=False, unique=True)

    # 用于封号
    valid = db.Column(db.SMALLINT, default=USER_NOT_FORBIDDEN)

    # 昵称, 默认为帐号名
    nickname = db.Column(db.String(20), default=account)

    # 性别
    gender = db.Column(db.SMALLINT)

    # 个人说明
    profile = db.Column(db.String(40))

    # 生日
    birthday = db.Column(db.TIMESTAMP, default=None)

    # token
    token = db.Column(db.String(6), default="000000")

    # ========== 关系 ==========

    # 该用户做出过的评论
    comments = db.relationship("Comment", backref="user", lazy="dynamic")

    # 该用户点过的赞
    thumb_ups = db.relationship("ThumbUp", backref="user", lazy="dynamic")

    # 该用户发表过的Post
    posts = db.relationship("Post", backref="user", lazy="dynamic")

    # ========== 关系 ==========

    def __repr__(self):
        return "<User %r %r %r>" % (self.account, self.nickname, self.token)

# 互动区域的吹水, 或者活动发布都可以
class Post(db.Model):

    # 话题, 用户自发的
    POST_TYPE_TOPIC = 1

    # 宣传活动性质的(公众号推文)
    POST_TYPE_ACTIVITY = 2

    __tablename__ = "posts"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 类型
    post_type = db.Column(db.SMALLINT, nullable=False)

    # 标题
    title = db.Column(db.String(40))

    # 描述信息(比如说公众号的推文的描述信息)
    description = db.Column(db.String(140))

    # 内容
    content = db.Column(db.TEXT)

    # 发布时间
    post_time = db.Column(db.TIMESTAMP, nullable=False)

    # 发布者(外键)
    uid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # ========== 关系 ==========

    # 这篇文章得到的评论
    comments = db.relationship("Comment", backref="post")

    # 这篇文章得到的赞
    thumb_ups = db.relationship("ThumbUp", backref="post")

    # ========== 关系 ==========

    def __repr__(self):
        return "<Post {username}> - {content}".format(username=self.user.account, content=self.content)


# 评论
class Comment(db.Model):

    __tablename__ = "comments"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 评论时间, 自动更新
    post_time = db.Column(db.TIMESTAMP, nullable=False)

    # 评论内容
    comment = db.Column(db.String(140))

    # 评论的对象
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    # 评论的发布者
    uid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return "<Comment {username}> - {content}".format(username=self.user.account, content=self.comment)


# 点赞
class ThumbUp(db.Model):

    __tablename__ = "thumb_ups"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 评论时间, 自动更新
    post_time = db.Column(db.TIMESTAMP, nullable=False)

    # 点赞的对象
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    # 点赞的人
    uid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return "<ThumbUp from {} to {}>".format(self.user.account, self.post.title)
