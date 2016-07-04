# coding=utf-8
__author__ = 'smallfly'

import sys
import logging
import os
from gevent import monkey
# 修改为异步
monkey.patch_all()

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, os.path.dirname(__file__))

# application 是 uwsgi 所需的默认名字
from app import app as application, db
# 尝试解决 MySQL server has gone away 的问题
application.config["SQLALCHEMY_POOL_RECYCLE"] = 5
db.create_all()
application.debug = False

if __name__ == "__main__":
    # 记得把 debug 关闭
	application.run(host="0.0.0.0", port=8080, debug=False)

