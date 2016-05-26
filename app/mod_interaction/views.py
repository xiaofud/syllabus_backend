# coding=utf-8
__author__ = 'smallfly'

from flask.views import View
from flask import render_template, request, jsonify
from app.mod_interaction.resources import helpers


class BannerView(View):

    # 允许使用的方法
    methods = ['GET', 'POST']

    def dispatch_request(self):

        # notification = {
        #     "id": i,
        #     "url": url,
        #     "link": link,
        #     "description": description
        # }
        if request.method == 'GET':
            banner = helpers.get_notification()
            return render_template("banners.html", banner=banner)
        elif request.method == 'POST':
            if helpers.make_notification(request.form.getlist('url'), request.form.getlist('link'), request.form.getlist('desc')):
                return jsonify(status="ok")
            else:
                return jsonify(status="failed")