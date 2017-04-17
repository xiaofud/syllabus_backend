# coding=utf-8
__author__ = 'smallfly'

from flask import render_template, request, jsonify, redirect
from app import app
from app.mod_interaction.resources import helpers

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/version")
def version():
    return render_template("version.html", version=helpers.load_version())

# Empty location when deployed behind Nginx
# Not sure the reason yet. Use Nginx server for a workaround now.
# ANDROID_REDIRECT_URI = 'stu://syllabus:80/login'
# IOS_REDIRECT_URI = 'stuclass://'
#
# # curl http://localhost:8080/oauth2_android?code=1234 -i
# @app.route("/oauth2_android", methods=['GET'])
# def oauth2_android():
#     if request.method == 'GET':
#         if "code" not in request.args:
#             print("Missing code in args")
#             return jsonify(msg="bad request"), 400
#         return redirect(ANDROID_REDIRECT_URI + "?code=" + request.args["code"])
#
# # curl http://localhost:8080/oauth2_ios?code=1234 -i
# @app.route("/oauth2_ios", methods=['GET'])
# def oauth2_ios():
#     if request.method == 'GET':
#         if "code" not in request.args:
#             print("Missing code in args")
#             return jsonify(msg="bad request"), 400
#         return redirect(IOS_REDIRECT_URI + "?code=" + request.args["code"])