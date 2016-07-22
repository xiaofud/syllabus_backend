# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource, fields, marshal
from flask_restful.reqparse import RequestParser
from app.mod_interaction.database_operations import common
from app.mod_interaction import models
from app.mod_interaction.resources.helpers import timestamp_to_string
from app.mod_interaction.resources import PassengerResource
from app import db

import time

# 返回的JSON结构
CARPOOL_STRUCTURE = {
    "id": fields.Integer,
    "uid": fields.Integer,
    "departure_time": fields.String,
    "driver": fields.String,
    "contact": fields.String,
    "source": fields.String,
    "destination": fields.String,
    "notice": fields.String,
    "max_people": fields.Integer,
    "people_count": fields.Integer,
    "passengers": fields.List(fields.Nested(PassengerResource.PASSENGER_STRUCTURE))
}

class CarpoolResource(Resource):

    """
    单个拼车信息
    """

    QUERY_BY_ID = 0 # 根据id获取拼车信息
    QUERY_BY_USER_ID = 1    # 根据用户获取拼车信息

    GET_PARSER = RequestParser(trim=True)
    POST_PARSER = RequestParser(trim=True)
    PUT_PARSER = RequestParser(trim=True)
    DELETE_PARSER = RequestParser(trim=True)

    def get(self):
        """
        获取拼车信息
        API请求地址:
        /interaction/api/v2/carpool
        方法: GET
        参数:
        type 可选, 默认为0, 位置: query参数, 0 表示按照拼车id获取拼车信息(即返回指定的单个拼车信息)
        id  位置: query参数, 值意为用户的uid, 或者拼车信息的id(由参数type决定)
        """
        # 决定搜索类型
        self.GET_PARSER.add_argument("type", type=int, location="args")
        self.GET_PARSER.add_argument("id", required=True, type=int, location="args")

        args = self.GET_PARSER.parse_args()
        # 默认按照拼车id寻找
        type_ = args["type"] or self.QUERY_BY_ID
        id_ = args['id']

        if type_ == self.QUERY_BY_ID:
            carpool = common.query_single_by_id(models.Carpool, id_)
            if carpool is not None:
                return marshal(carpool, CARPOOL_STRUCTURE)
            else:
                return {"error": "not found"}, 404
        else:
            carpools = models.Carpool.query\
                .join(models.Passenger, models.Carpool.id == models.Passenger.carpool_id)\
                .filter(models.Passenger.uid == id_)\
                .all()
            if len(carpools) == 0:
                return {"error": "not found"}, 404
            else:
                return marshal(carpools, CARPOOL_STRUCTURE)


    def post(self):
        """
        发布拼车信息
        API请求地址:
        /interaction/api/v2/carpool
        方法: POST
        参数: 所有参数位置为form, 即 URL-ENCODED 的字符串
        必选参数:
            uid 发布拼车信息的用户的id
            token 用户的token
            departure_time 发车时间, 为[时间戳]
            driver 司机信息, 字符串
            contact 用户自己的联系信息, 存储JSON字符串, 和iOS端沟通好结构
                例: {"wechat": "xxx", "phone": xxx} 等, 方便用于复制联系信息到剪贴板
            source 出发地点
            destination 目的地
            max_people 这辆车最多能坐多少人
        可选参数:
            notice 备注信息, 如哪里集合之类的
        """

        # 验证信息
        self.POST_PARSER.add_argument("uid", type=int, required=True, location="form")
        self.POST_PARSER.add_argument("token", required=True, location="form")
        # 具体数据
        self.POST_PARSER.add_argument("departure_time", type=int, required=True, location="form")
        self.POST_PARSER.add_argument("driver", required=True, location="form")
        self.POST_PARSER.add_argument("contact", required=True, location="form")
        self.POST_PARSER.add_argument("source", required=True, location="form")
        self.POST_PARSER.add_argument("destination", required=True, location="form")

        self.POST_PARSER.add_argument("notice", required=False, location="form")

        self.POST_PARSER.add_argument("max_people", required=True, location="form")
        # self.POST_PARSER.add_argument("people_count")

        args = self.POST_PARSER.parse_args()

        # 检查token
        if not common.check_token(args):
            return {"error": "wrong token"}, 401

        del args["token"]

        args["departure_time"] = timestamp_to_string(args["departure_time"])

        carpool = models.Carpool(**args)

        # print(carpool)
        if common.add_to_db(db, carpool) == True:
            # 这里还要添加一条记录到 Passenger 里
            now = timestamp_to_string(int(time.time()))
            passenger = models.Passenger(join_time=now,
                                         uid=args["uid"],
                                         carpool_id=carpool.id,
                                         contact=args["contact"]
            )
            common.add_to_db(db, passenger)
            return {"id": carpool.id}, 200
        else:
            return {"error": "Internal Server Error"}, 500

    def put(self):

        """
        更新拼车信息
        API请求地址:
        /interaction/api/v2/carpool
        方法: PUT
        参数: 所有参数位置为form, 即 URL-ENCODED 的字符串
        必选参数:
            id 拼车信息的id
            uid 发布拼车信息的用户的id
            token 用户的token
            departure_time 发车时间, 为[时间戳]
            driver 司机信息, 字符串
            contact 用户自己的联系信息, 存储JSON字符串, 和iOS端沟通好结构
                例: {"wechat": "xxx", "phone": xxx} 等, 方便用于复制联系信息到剪贴板
            source 出发地点
            destination 目的地
            max_people 这辆车最多能坐多少人
        可选参数:
            notice 备注信息, 如哪里集合之类的
        """

        # 验证信息
        self.PUT_PARSER.add_argument("uid", type=int, required=True, location="form")
        self.PUT_PARSER.add_argument("token", required=True, location="form")
        # 具体数据
        self.PUT_PARSER.add_argument("departure_time", type=int, required=True, location="form")
        self.PUT_PARSER.add_argument("driver", required=True, location="form")
        self.PUT_PARSER.add_argument("contact", required=True, location="form")
        self.PUT_PARSER.add_argument("source", required=True, location="form")
        self.PUT_PARSER.add_argument("destination", required=True, location="form")

        self.PUT_PARSER.add_argument("notice", required=False, location="form")

        self.PUT_PARSER.add_argument("max_people", required=True, location="form")

        self.PUT_PARSER.add_argument("id", type=int, required=True, location="form")

        args = self.PUT_PARSER.parse_args(strict=True)
        # print(args)
        # 检查token
        if not common.check_token(args):
            return {"error": "wrong token"}, 401

        # 去掉其他辅助信息
        del args["token"]

        id_ = args["id"]
        del args["id"]

        uid = args["uid"]
        del args["uid"]

        args["departure_time"] = timestamp_to_string(args["departure_time"])

        status = common.update_model_by_id(models.Carpool, db, id_, uid, **args)
        if status == True:
            return {"status": "updated"}
        else:
            code = status[1]
            if code == common.ERROR_NOT_FOUND:
                return {"error": "not found"}, 404
            elif code == common.ERROR_USER_ID_CONFLICT:
                return {"error": "forbidden"}, 403
            elif code == common.ERROR_COMMIT_FAILED:
                return {"error": "Internal Server Error"}, 500

    def delete(self):
        """
        删除拼车信息
        API请求地址:
        /interaction/api/v2/carpool
        方法: DELETE
        参数: 所有参数位于请求头部
        必选参数:
            id 拼车信息的id
            uid 发布拼车信息的用户id(发布者才有权删除)
            token 用户的token
        """

        self.DELETE_PARSER.add_argument("id", type=int, required=True, location="headers")
        self.DELETE_PARSER.add_argument("uid", type=int, required=True, location="headers")
        self.DELETE_PARSER.add_argument("token", required=True, location="headers")

        args = self.DELETE_PARSER.parse_args()

        # 检查token
        if not common.check_token(args):
            return {"error": "wrong token"}, 401

        status = common.delete_from_db(db, models.Carpool, args["id"], args["uid"])
        if status == True:
            return {"status": "deleted"}
        else:
            code = status[1]
            if code == common.ERROR_NOT_FOUND:
                return {"error": "not found"}, 404
            elif code == common.ERROR_USER_ID_CONFLICT:
                return {"error": "forbidden"}, 403
            elif code == common.ERROR_COMMIT_FAILED:
                return {"error": "Internal Server Error"}, 500


class CarpoolSResource(Resource):
    """
    获取多个拼车消息
    """

    # 有无司机
    # HAS_DRIVER = 1
    # HAS_NOT_DRIVER = 2

    GET_PARSER = RequestParser(trim=True)

    def query(self, arg_dict):


        # 分页 http://my.oschina.net/ranvane/blog/196906

        # 按照各种条件搜索拼车
        # query_obj = models.Carpool.query

        # 读取条件
        now = timestamp_to_string(int(time.time()))
        # 设置时间条件
        depart_time = arg_dict["depart_time"] or now

        # print(depart_time)

        page_index = arg_dict["page_index"] or 1

        page_size = arg_dict["page_size"] or 10

        page_obj = \
            models.Carpool.query\
                .filter(models.Carpool.departure_time >= depart_time)\
                .order_by(models.Carpool.departure_time.asc())\
                .order_by(models.Carpool.people_count.desc())\
                .paginate(page_index, page_size, False)

        carpools = page_obj.items

        # print(len(carpools))

        return carpools





    def get(self):
        """
        更新拼车信息
        API请求地址:
        /interaction/api/v2/carpools
        方法: GET
        参数: 所有参数为query参数
        可选参数:
            depart_time 出发时间戳, 返回结果中将只会返回出发时间等于或者大于这个时间的拼车信息
            page_index 页数
            page_size 一页返回的数量
        """
        self.GET_PARSER.add_argument("depart_time", type=int, location="args")
        # DRIVER 由客户端判断
        # self.GET_PARSER.add_argument("driver", type=int, location="args")
        # 已经有的人数, 由客户端判断
        # self.GET_PARSER.add_argument("count", type=int, location="args")
        # 用于分页
        self.GET_PARSER.add_argument("page_index", type=int, location="args")
        # 用于分页
        self.GET_PARSER.add_argument("page_size", type=int, location="args")

        # 排序相关
        # 排序关键字
        # self.GET_PARSER.add_argument("sort_by", action="append", location="args")
        # 排序顺序
        # self.GET_PARSER.add_argument("order", action="append", location="args")

        args = self.GET_PARSER.parse_args()

        carpools = self.query(args)

        print(len(carpools))

        if len(carpools) > 0:
            return marshal(carpools, CARPOOL_STRUCTURE)
        else:
            return {"error": "nothing found"}, 404

