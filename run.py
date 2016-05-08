# coding=utf-8
__author__ = 'smallfly'

from app import app, db

db.create_all()
app.run(host="0.0.0.0", port=8080, debug=True)
