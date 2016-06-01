# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, reqparse, fields, marshal
from flask import jsonify
from app.mod_interaction.database_operations import common
from app.mod_interaction.models import User, UnRead, Post
from app.mod_interaction.resources import PostResource
from app import db


class UnreadResource(Resource):

    GET_PARSER = reqparse.RequestParser(trim=True)
    DELETE_PARSER = reqparse.RequestParser(trim=True)

    RETURN_POST_ID_LIST = 0 # 默认行为, 仅返回未读信息的一系列post_id
    RETURN_POST_LIST = 1    # 返回未读信息(post_list)


    def get(self):
        """
        测试:
        参数: uid, type(可选, 0(默认值) - 获取post_id; 1 - 获取对应的 post, 返回值与 get post 返回值一致)
        curl "localhost:8080/interaction/api/v2/unread?uid=1&type=0"    # type 默认为 0
        curl "localhost:8080/interaction/api/v2/unread?uid=1&type=1"
        :return:
        可能返回值:
        404, 表示没有该用户, 或者该用户并没有未读信息
        200, {"messages": [1, 2, 3,...]}, 一系列post_id
        200, {"post_list": []} post 数组, 同 get post 返回值格式
        """
        self.GET_PARSER.add_argument("uid", required=True, type=int, location="args")
        self.GET_PARSER.add_argument("type", type=int, default=0, location="args")

        args = self.GET_PARSER.parse_args()

        # 找到对应的用户
        user = User.query.filter_by(id=args["uid"]).first()
        if user is None:
            return {"error": "no such user found"}, 404

        # 获取 该用户的 post_ids

        unread_messages = UnRead.query.with_entities(UnRead.post_id).filter_by(uid=args["uid"]).all()
        if len(unread_messages) == 0:
                return {"error": "no unread messages"}, 404

        post_ids = list(map(lambda x: x.post_id, unread_messages))


        if args["type"] == self.RETURN_POST_LIST:
            posts = Post.query.filter(Post.id.in_(set(post_ids))).all()
            return marshal(posts, PostResource.SINGLE_POST_STRUCTURE, "post_list")
        else:
            return jsonify(messages=post_ids)

        
    def delete(self):
        """
        测试:
        参数: uid, pid(post_id, 报头中貌似使用下划线会有一些问题, 所以改为pid), token
        curl "localhost:8080/interaction/api/v2/unread" -X DELETE -H "token: 000000" -H "uid: 2" -H "pid: 2"
        # 注意这里是pid, header 中貌似使用 _ 会有一些遗留问题
        http://stackoverflow.com/questions/22856136/why-underscores-are-forbidden-in-http-header-names
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

