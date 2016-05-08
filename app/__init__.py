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
from app.mod_credit import credit_blueprint

app.register_blueprint(interaction_blueprint)
app.register_blueprint(credit_blueprint)

# 404
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404   # 一定记得返回 404 code

# 不要在这里建立数据库
# db.drop_all()
# db.create_all()

