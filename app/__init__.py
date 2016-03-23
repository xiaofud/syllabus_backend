# coding=utf-8
__author__ = 'smallfly'

from flask import Flask, jsonify
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

# 404
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e))

# print(db.get_tables_for_bind())
db.drop_all()
db.create_all()

from app.mod_interaction.models import *
# 建立一些测试用途的数据
def generate_test_data():
    # 一些测试数据

    import json
    photo_list = {
        "1": "https://xiaofud.me/img/img0082.jpg",
        "2": "https://xiaofud.me/img/img0082.jpg"
    }
    photo_list_json = json.dumps(photo_list, ensure_ascii=True)

    for i in range(10):

        user_info = {
            "account": "14xfdeng " + str(i),
            "nickname": "xiaofud" + str(i),
            "birthday": "1995-12-23",
            "gender": 1,
            "profile": "hello world"
        }
        user = User(**user_info)

        db.session.add(user)
        db.session.commit()

        post_info = {
            "post_type": 1,
            "uid": user.id,
            "title": "this is title",
            "content": "this is content",
            "description": "this is description",
            "photo_list_json": photo_list_json
        }

        post = Post(**post_info)

        db.session.add(post)
        db.session.commit()

        comment_info = {
            "post_id": 1,
            "uid": user.id,
            "comment": "comment"
        }
        comment = Comment(**comment_info)

        db.session.add(comment)
        db.session.commit()

        like_info = {
            "uid": user.id,
            "post_id": 1
        }

        like = ThumbUp(**like_info)

        db.session.add(like)
        db.session.commit()


generate_test_data()