# coding=utf-8
__author__ = 'smallfly'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
import datetime
import os

from config import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = \
    config["SQLALCHEMY_DATABASE_URI"]    # 这是默认的数据库连接

# 从旧的数据库中读取数据
DIR_PATH = os.path.dirname(__file__)
DATA_BASE_NAME = "syllabus.db"
FILE_NAME = os.path.join(DIR_PATH, DATA_BASE_NAME).replace("\\", "/")
DATA_BASE_URI = "sqlite:///" + FILE_NAME
app.config["SQLALCHEMY_BINDS"] = {  # 这里定义了其他的数据库连接
    "sqlite3": DATA_BASE_URI
}

# 从旧的数据库中读取数据

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

USER_NAME_LENGTH = 20
CERTIFICATE_LENGTH = 6     # 6个数字组成的认证码

class UserModel(db.Model):
    # 最小结构即可
    __tablename__ = "user_table"
    __bind_key__ = "sqlite3"    # 指明是哪个数据库连接, 如果没有指定, 则使用 SQLALCHEMY_DATABASE_URI 指定的数据库连接

    # 基本字段
    id = db.Column(db.Integer, primary_key=True)

    # 用户账号
    user_account = db.Column(db.String(USER_NAME_LENGTH), unique=True)

    # 凭证 6 个随机数字组成的认证码
    user_certificate = db.Column(db.String(CERTIFICATE_LENGTH))

    # 用户的昵称
    user_nickname = db.Column(db.String(20))    # 如果没有提供的话 那就是 null



    def __repr__(self):
        return "<User %r %r>" % (self.user_account, self.user_certificate)

class User(db.Model):
    # 最小结构即可
    __tablename__ = "users" # 表名

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 用户账号
    account = db.Column(db.String(20), nullable=False, unique=True)

    # 昵称
    nickname = db.Column(db.String(20))

    # token
    token = db.Column(db.String(6), default="000000")

    def __repr__(self):
        return "<User %r %r %r>" % (self.account, self.nickname, self.token)


def generate_token(length=6):
    random_str = ""
    for i in range(length):
        num = random.randint(0, 9)
        random_str += str(num)
    return random_str

def insert_people():
    account = input("input the account: ")
    nickname = input("input nickname: ")

    birthday = datetime.datetime.now().strftime("%Y/%m/%d")
    # print(birthday)

    token = generate_token(6)
    # print(token)

    user = User(account=account, nickname=nickname, birthday=birthday, token=token)
    print(user)

def sqlite3_to_mysql_user():
    # sqlite3_users = UserModel.query.distinct(UserModel.user_account).all()
    sqlite3_users = UserModel.query.all()
    # 因为之前有一些末尾有空格的错误数据, 所以需要处理一下

    print(len(sqlite3_users))

    for sqlite3_user in sqlite3_users:
        account = sqlite3_user.user_account.strip()
        nickname =  sqlite3_user.user_nickname.strip()
        token = sqlite3_user.user_certificate
        user = User(account=account, nickname=nickname, token=token)
        # print(user)
        try:
            # 这样会很慢, 但是因为之前有些数据有问题, 只能如此
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

if __name__ == "__main__":
    sqlite3_to_mysql_user()




