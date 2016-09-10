# coding=utf-8
__author__ = 'smallfly'

import os
import time

from flask.views import View
from flask import render_template, request, jsonify, abort
from app.mod_interaction.resources import helpers
from app import app

class BannerView(View):

    # 允许使用的方法
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'GET':
            banner = helpers.get_notification()
            return render_template("banners.html", banner=banner)
        elif request.method == 'POST':
            if helpers.make_notification(request.form.getlist('url'), request.form.getlist('link'), request.form.getlist('desc')):
                return jsonify(status="ok")
            else:
                return jsonify(status="failed")

class UploadBannerView(View):

    methods = ["GET", "POST"]

    def dispatch_request(self):
        if request.method == 'GET':
            return render_template("uploadBanner.html")
        else:
            files = request.files
            if "image" not in files:
                print("abort 400")
                abort(400)
            file = files["image"]
            name, extension = os.path.splitext(file.filename)
            if extension.strip() == "":
                abort(400)
            filename = "banner_" + str(int(time.time())) + extension
            try:
                file.save(os.path.join(app.config["BANNER_UPLOAD_DIR"], filename))
                url = "http://119.29.95.245:8000/" + filename
                return jsonify(status="succeed", URL=url)
            except Exception as e:
                print(e)
                return jsonify(ERROR=str(e))

