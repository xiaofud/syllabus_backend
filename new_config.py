# coding=utf-8
__author__ = 'smallfly'
# 用于生成新的配置文件


import json

config = dict()
# 一些默认数据
config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 一些默认数据
config["SQLALCHEMY_DATABASE_URI"] = input("DATABASE_URI: ")
config["SECRET_KEY"] = input("SECRET_KEY: ")

with open("config.conf", "w") as f:
    json.dump(config, f)