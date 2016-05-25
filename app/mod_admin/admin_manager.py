# coding=utf-8
__author__ = 'smallfly'

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import db
from app.mod_interaction import models

admin = Admin(name="syllabus", template_mode='bootstrap3')
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Post, db.session))
