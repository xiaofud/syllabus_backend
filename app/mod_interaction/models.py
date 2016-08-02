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

    LEVEL_NORMAL = 0    # 普通权限
    LEVEL_CAN_POST_ACTIVITY = 1 # 可以发布活动信息
    LEVEL_MANAGER = 2   # 管理员权限, 可以删除任意信息


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

    # 记录用户权限
    level = db.Column(db.SMALLINT, default=LEVEL_NORMAL)

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

    # (公众号推文)
    POST_TYPE_ACTIVITY = 1  # 如果是这种类型的话, 那么客户端处理的时候就要注意把content作为文章的URL

    # 校园活动的文章, 类似于推文
    # content视为URL, description为描述信息
    POST_TYPE_SCHOOL_ACTIVITY = 2

    __tablename__ = "posts"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 类型
    post_type = db.Column(db.SMALLINT, nullable=False)

    # 描述信息(比如说公众号的推文的描述信息)
    description = db.Column(db.String(140))

    # 内容
    content = db.Column(db.TEXT)


    # 用户同时上传的图片列表, 存储原始的json数据
    photo_list_json = db.Column(db.TEXT)

    # 发布时间
    post_time = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())

    # 是否对外部可见
    visibility = db.Column(db.SMALLINT, default=VISIBILITY_VISIBLE)

    # 记录客户端系统, 如 iOS android, 也可以记录活动部门
    source = db.Column(db.VARCHAR(20), nullable=True)

    # =========== 活动相关 ===========
    # 活动开始时间
    activity_start_time = db.Column(db.TIMESTAMP, nullable=True)
    # 活动结束时间
    activity_end_time = db.Column(db.TIMESTAMP, nullable=True)
    # 活动地点
    activity_location = db.Column(db.VARCHAR(40), nullable=True)

    # =========== 活动相关 ===========

    # 发布者(外键)
    uid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # ========== 关系 ==========

    # 这篇文章得到的评论
    # cascade="all, delete-orphan", 表示删除这个文章的时候将会删除所有与之关联起来的对象
    # primaryjoin 指明 join 的条件
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan",
                               primaryjoin="and_(Post.id==Comment.post_id, Comment.visibility==1)")


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
    post_time = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())

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
    post_time = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())

    # 点赞的对象
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    # 点赞的人
    uid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # 是否对外部可见
    # visibility = db.Column(db.SMALLINT, default=VISIBILITY_VISIBLE)

    def __repr__(self):
        return "<ThumbUp from {} to {}>".format(self.user.account, self.post.title)

class Carpool(db.Model):

    """
    拼车信息
    """

    __tablename__ = "carpools"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 发起拼车的童鞋
    uid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # 司机信息
    driver = db.Column(db.VARCHAR(50), nullable=True)

    # 自己的联系方式
    contact = db.Column(db.VARCHAR(200), nullable=True)

    # 出发地
    source = db.Column(db.VARCHAR(50), nullable=False)

    # 目的地
    destination = db.Column(db.VARCHAR(50), nullable=False)

    # 出发时间
    departure_time = db.Column(db.TIMESTAMP, default=None)

    # 备注
    notice = db.Column(db.VARCHAR(200))

    # 最多允许几个人拼车, 默认4人
    max_people = db.Column(db.SMALLINT, default=4)

    # 目前拼车人数
    people_count = db.Column(db.SMALLINT, default=1)

    # JOIN
    passengers = db.relationship("Passenger", backref="carpool", lazy="dynamic")

    def __repr__(self):
        return "<Carpool uid: {} {}/{}".format(self.uid, self.people_count, self.max_people)


class Passenger(db.Model):

    """
    拼车的用户
    """

    __tablename__ = "passengers"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 发起拼车的童鞋
    uid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # 拼车信息id
    carpool_id = db.Column(db.Integer, db.ForeignKey("carpools.id"), nullable=False)

    # join time
    join_time = db.Column(db.TIMESTAMP, default=None)

    # 自己的联系方式(用json方式存储)
    contact = db.Column(db.VARCHAR(200), nullable=True)

    def __repr__(self):
        return "<Passenger uid:{} contact:{}".format(self.uid, self.contact)

# 未读资源
class UnRead(db.Model):
    """
    每条记录有 uid, post_id 两个外键, 表明
    用户uid在post_id这篇文章内有未读的动态.
    """
    __tablename__ = "unreads"

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    uid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # 点赞的对象
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def __repr__(self):
        return "<UnRead uid: %r pid: %r>" % (self.uid, self.post_id)

# 新的表
# class Shop(db.Model):
#
#     __tablename__ = "shops"
#
#     # 主键
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#
#     # 店名
#     name = db.Column(db.VARCHAR(40), nullable=False)
#
#     # 电话
#     phone = db.Column(db.VARCHAR(20), nullable=False)
#
#     # Website
#     website = db.Column(db.VARCHAR(120), nullable=False)