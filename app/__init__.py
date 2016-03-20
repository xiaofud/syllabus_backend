# coding=utf-8
__author__ = 'smallfly'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# 读取配置文件
import config

app = Flask(__name__)
app.config.update(config.config)
db = SQLAlchemy(app)


# 注意要等db已经建立好之后, 再去import blueprint, 因为blueprint里面需要app的db
# 注册blueprint
from app.mod_interaction import interaction_blueprint
app.register_blueprint(interaction_blueprint)

# print(db.get_tables_for_bind())
db.drop_all()
db.create_all()

# 一些测试数据
from app.mod_interaction.models import *
user_info = {
    "account": "14xfdeng",
    "nickname": "xiaofud",
    "birthday": "1995-12-23",
    "gender": 1,
    "profile": "hello world"
}
user = User(**user_info)

db.session.add(user)
db.session.commit()

post_info = {
    "post_type": user.id,
    "uid": 1,
    "title": "this is title",
    "content": "this is content",
    "description": "this is description"
}

post = Post(**post_info)

db.session.add(post)
db.session.commit()