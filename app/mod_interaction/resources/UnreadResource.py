# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, reqparse, fields, marshal
from flask import jsonify
from app.mod_interaction.database_operations import common
from app.mod_interaction.models import User, UnRead
from app import db


class UnreadResource(Resource):

    GET_PARSER = reqparse.RequestParser(trim=True)
    DELETE_PARSER = reqparse.RequestParser(trim=True)

    def get(self):
        """
        获取uid指向的用户的未读消息
        返回情况
        404, 两种情况, 一是没有未读消息, 而是该用户不存在
        200, messages数组, 一系列
        :return:
        """
        self.GET_PARSER.add_argument("uid", required=True, type=int, location="args")
        args = self.GET_PARSER.parse_args()
        user = User.query.filter_by(id=args["uid"]).first()
        if user is not None:
            unread_messages = UnRead.query.with_entities(UnRead.post_id).filter_by(uid=args["uid"]).all()
            if len(unread_messages) == 0:
                return {"error": "no unread messages"}, 404
            post_ids = list(map(lambda x: x.post_id, unread_messages))
            return jsonify(messages=post_ids)
        else:
            return {"error": "no such user found"}, 404
        
    def delete(self):
        """
        curl "localhost:8080/interaction/api/v2/unread" -X DELETE -H "token: 000000" -H "uid: 2" -H "pid: 2"
        :return:
        """
        self.DELETE_PARSER.add_argument("token", required=True, location="headers")
        self.DELETE_PARSER.add_argument("uid", type=int, required=True, location="headers")
        # 貌似头部的key不能有下划线
        self.DELETE_PARSER.add_argument("pid", type=int, required=True, location="headers")

        args = self.DELETE_PARSER.parse_args()

        # 检查token
        if common.check_token(args):
            # print(args)
            unread_message = UnRead.query.filter_by(uid=args["uid"]).filter_by(post_id=args["pid"]).all()
            # print("len of message", len(unread_message))
            for message in unread_message:
                # common.delete_from_db(db, UnRead, )
                # print(message)
                db.session.delete(message)
            try:
                db.session.commit()
                return {"status": "deleted"}, 200
            except Exception as e:
                print("error when remove unreads:", repr(e))
                db.session.rollback()
                return {"error": repr(e)}, 500
        else:
            return {"error": "unauthorized"}, 401

