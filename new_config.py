# coding=utf-8
__author__ = 'smallfly'
# 用于生成新的配置文件


import json
import os

CUR_DIR = os.path.dirname(__file__)

config = dict()
# 一些默认数据
config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 一些默认数据
config["SQLALCHEMY_DATABASE_URI"] = input("DATABASE_URI: ")
config["SECRET_KEY"] = input("SECRET_KEY: ")

config_file = os.path.join(CUR_DIR, "config.conf")

with open(config_file, "w") as f:
    json.dump(config, f)