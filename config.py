# coding=utf-8
import os, json

config = dict()

# Statement for enabling the development environment
config["DEBUG"] = False

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
config["BASE_DIR"] = BASE_DIR
# 保存更新信息的文件夹
config["VERSION_DIR"] = BASE_DIR + os.path.sep + "versions"
config["BANNER_DIR"] = BASE_DIR + os.path.sep + "banners"
config["BANNER_UPLOAD_DIR"] = "/home/hjxf/share_folder"
# 存放公告文件的文件夹
config["NOTICE_DIR"] = BASE_DIR + os.path.sep + "notice"
# 最大文件为1MB
config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# private settings
with open(os.path.join(BASE_DIR, "config.conf")) as f:
    config.update(json.load(f))

