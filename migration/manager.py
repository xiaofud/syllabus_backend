# coding=utf-8
__author__ = 'smallfly'

# 用于更新数据库
# http://flask-migrate.readthedocs.io/en/latest/

"""
基本用法
首先运行
Initializes migration support for the application.
python3 manager.py db init 让 migrate 为该 app 创建数据库迁移支持

然后修改了数据库表的信息之后执行
python3 manager.py db migrate --message "message"
程序会检测到数据库有变化, 同时生成一个新的版本文件
里面有这次变动的详细信息, 包括如何升级以及如何降级
可以用
python3 manager.py db edit 去修改这次改动

一切无误之后
python3 manager.py db upgrade
即可对表的修改生效了

更多详细用法参考文档
http://flask-migrate.readthedocs.io/en/latest/
"""

import sys
import os
# 这里最好用一下绝对路径
PRE_DIR = os.path.dirname(os.path.abspath(__file__))
PRE_DIR = os.path.dirname(PRE_DIR)
sys.path.insert(0, PRE_DIR)

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()