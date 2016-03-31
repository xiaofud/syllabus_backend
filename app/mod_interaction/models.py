# coding=utf-8
__author__ = 'smallfly'

from app import db

SUPER_USERS = [
    "14xfdeng",
    "14jhwang",
    "13yjli3"
]

VISIBILITY_VISIBLE = 1
VISIBILITY_INVISIBLE = 2

# 用户表
class User(db.Model):

    # 性别常量
    GENDER_FEMALE = 0
    GENDER_MALE = 1
    GENDER_UNKNOWN = -1

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
    nickname = db.Column(db.String(20), default=account, unique=True)

    # 性别
    gender = db.Column(db.SMALLINT, default=GENDER_UNKNOWN)

    # 个人说明
    profile = db.Column(db.String(40))

    # 生日
    birthday = db.Column(db.TIMESTAMP, default=None)

    # token
    token = db.Column(db.String(6), default="000000")

    # 头像地址
    image = db.Column(db.String(128))

    # 是否对外部可见
    visibility = db.Column(db.SMALLINT, default=VISIBILITY_VISIBLE)

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
    POST_TYPE_TOPIC = 0

    # 宣传活动性质的(公众号推文)
    POST_TYPE_ACTIVITY = 1  # 如果是这种类型的话, 那么客户端处理的时候就要注意把content作为文章的URL

    __tablename__ = "posts"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 类型
    post_type = db.Column(db.SMALLINT, nullable=False)

    # 标题
    # title = db.Column(db.String(40))

    # 描述信息(比如说公众号的推文的描述信息)
    description = db.Column(db.String(140))

    # 内容
    content = db.Column(db.TEXT)

    # 用户同时上传的图片列表, 存储原始的json数据
    photo_list_json = db.Column(db.TEXT)

    # 发布时间
    post_time = db.Column(db.TIMESTAMP, nullable=False)

    # 发布者(外键)
    uid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # 是否对外部可见
    visibility = db.Column(db.SMALLINT, default=VISIBILITY_VISIBLE)

    # ========== 关系 ==========

    # 这篇文章得到的评论
    # cascade="all, delete-orphan", 表示删除这个文章的时候将会删除所有与之关联起来的对象
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan")


    # 这篇文章得到的赞
    thumb_ups = db.relationship("ThumbUp", backref="post", cascade="all, delete-orphan")

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

    # 是否对外部可见
    visibility = db.Column(db.SMALLINT, default=VISIBILITY_VISIBLE)

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

    # 是否对外部可见
    visibility = db.Column(db.SMALLINT, default=VISIBILITY_VISIBLE)

    def __repr__(self):
        return "<ThumbUp from {} to {}>".format(self.user.account, self.post.title)
