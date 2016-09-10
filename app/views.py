# coding=utf-8
__author__ = 'smallfly'

from flask import render_template
from app import app
from app.mod_interaction.resources import helpers

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/version")
def version():
    return render_template("version.html", version=helpers.load_version())