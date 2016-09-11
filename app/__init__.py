# coding=utf-8
__author__ = 'smallfly'

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
# 读取配置文件
import config

# 相同目录下找 static 文件夹
app = Flask(__name__, static_folder='static')
app.config.update(config.config)
# 设置 mysql 编码为 utf8mb4
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)


from app.mod_admin.admin_manager import admin
admin.init_app(app)

# 注意要等db已经建立好之后, 再去import blueprint, 因为blueprint里面需要app的db
# 注册blueprint
from app.mod_interaction import interaction_blueprint
from app.mod_interaction.api_v2_1 import interaction_blueprint2_1
from app.mod_credit import credit_blueprint

app.register_blueprint(interaction_blueprint)
app.register_blueprint(interaction_blueprint2_1)
app.register_blueprint(credit_blueprint)


# 导入views
from app import views

# 404
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404   # 一定记得返回 404 code

# 不要在这里建立数据库
# db.drop_all()
# db.create_all()

