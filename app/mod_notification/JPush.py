# coding=utf-8
__author__ = 'smallfly'

"""
用于推送JPush消息
http://docs.jpush.io/server/rest_api_v3_push/
"""

import requests
from requests.auth import HTTPBasicAuth

ACCEPT_PLATFORMS = {"android", "ios", "winphone"}

class JPush(object):

    # 推送API
    PUSH_URL = "https://api.jpush.cn/v3/push"

    # 报告API
    REPORT_URL = "https://report.jpush.cn"
    # 检测消息接收的条数
    RECEIVED = "/v3/received"

    # 设备API
    DEVICE_URL = "https://device.jpush.cn"
    TAGS_URL = "/v3/tags/"

    def __init__(self, appkey, master_key):
        if appkey is None or master_key is None:
            raise ValueError("appkey, master_key can't be None")
        self.appkey = appkey
        self.master_key = master_key
        self.httpAuth = HTTPBasicAuth(self.appkey, self.master_key)

    def push(self, platform="all", audience="all", default_alert="",android_spec=None, ios_spec=None, options=None):
        """
        像用户发送推送
        :param platform: 平台 "android", "ios", "winphone", "all", 可以用 ["android", "ios"] 这种形式推送到多个平台
        :param audience: all 或者是指定 alias "alias" : [ "4314", "892", "4531" ] 或者 tag: ["1", "2"] 等等
        :param default_alert: 推送的内容, 可以被 android_spec 或者 ios_spec 给覆盖
        :param android_spec: 可以使用build_custom_notification构建
        :param ios_spec: 可以使用build_custom_notification构建
        :return:
        """

        json_body = {
            "platform": platform,
            "audience": audience,
            "notification": {
                "alert": default_alert,
                "android": android_spec,
                "ios": ios_spec
            },
            "options": options
        }

        # 去掉没有提供的参数
        if android_spec is None:
            json_body["notification"].pop("android")
        if ios_spec is None:
            json_body["notification"].pop("ios")
        if options is None:
            json_body.pop("options")

        print(repr(json_body))

        resp = requests.post(JPush.PUSH_URL, json=json_body, auth=self.httpAuth)
        if resp.ok:
            print(resp.json())
            return resp.json()
        else:
            print(resp.status_code, resp.text)
            return None

    def getTags(self):
        resp = requests.get(JPush.DEVICE_URL + JPush.TAGS_URL, auth=self.httpAuth)
        if resp.ok:
            print(resp.json())
        else:
            print(resp.status_code, resp.json())

    def received(self, iterable_msg_id):
        msg_ids = ",".join(iterable_msg_id)
        args = {
            "msg_ids": msg_ids
        }
        resp = requests.get(JPush.REPORT_URL + JPush.RECEIVED, params=args, auth=self.httpAuth)
        if resp.ok:
            print(resp.json())
            return resp.json()
        else:
            print(resp.status_code, resp.json())
            return None

# ===========================辅助函数===========================

def build_custom_notification(alert=None, title=None, extras=None):
    """
    构建不同的自定义推送, 比如说针对安卓用户的提示, 会覆盖 notification 的设置
    :param alert: 消息内容
    :param title: 标题
    :param extras: 而外的内容, 要是json对象
    :return:
    """

    json_body = {
        "alert": alert,
        "title": title,
        "extras": extras
    }

    if alert is None:
        json_body.pop("alert")
    if title is None:
        json_body.pop("title")
    if extras is None:
        json_body.pop("extras")

    return json_body

def build_alias(aliases):
    return {
        "alias": aliases
    }

def build_tag(tags):
    return {
        "tag": tags
    }

def build_options(sendno=None, time_to_live_s=None, override_msg_id=None, apns_production=True, big_push_duration=None):
    """
    额外的设置选项
    :param sendno: 纯粹用来作为 API 调用标识，API 返回时被原样返回，以方便 API 调用方匹配请求与返回。
    :param time_to_live: 推送当前用户不在线时，为该用户保留多长时间的离线消息，以便其上线时再次推送。默认 86400 （1 天），最长 10 天。设置为 0 表示不保留离线消息，只有推送当前在线的用户可以收到。
    :param override_msg_id: 覆盖之前推送的消息, 1）该 msg_id 离线收到的消息是覆盖后的内容；2）即使该 msg_id Android 端用户已经收到，如果通知栏还未清除，则新的消息内容会覆盖之前这条通知；覆盖功能起作用的时限是：1 天。
    :param apns_production: True 表示推送生产环境，False 表示要推送开发环境；如果不指定则为推送生产环境。JPush 官方 API LIbrary (SDK) 默认设置为推送 “开发环境”。
    :param big_push_duration: 又名缓慢推送，把原本尽可能快的推送速度，降低下来，给定的n分钟内，均匀地向这次推送的目标用户推送。最大值为1400.未设置则不是定速推送。
调用返回
    :return:
    """
    json_obj = {
        "sendno": sendno,
        "time_to_live": time_to_live_s,
        "override_msg_id": override_msg_id,
        "apns_production": apns_production,
        "big_push_duration": big_push_duration
    }
    to_remove = []
    for key in json_obj:
        if json_obj[key] is None:
            to_remove.append(key)
    for key in to_remove:
        json_obj.pop(key)

    if json_obj:
        return json_obj
    else:
        return None

# ===========================辅助函数===========================

if __name__ == "__main__":
    import config_key
    app_key, master_key = config_key.read_key()
    print(app_key, master_key)
    jpush = JPush(app_key, master_key)
    extras = {
        "name": "xiaofud"
    }
    android_notification = \
        build_custom_notification(alert="这是测试内容", title="感觉不错哟", extras=extras)
    jpush.push(android_spec=android_notification)

    # jpush.push(default_alert="Hi! Surprise!!", android_spec=android_notification)
    # jpush.getTags()
    # audience = build_alias(["14xfdeng"])
    # resp = jpush.push(audience=audience, default_alert="Hello")
    # 覆盖信息
    # if resp is not None:
    #     msg_id = resp["msg_id"]
    #     options = build_options(override_msg_id=msg_id)
    #     print(options)
    #     jpush.push(audience=audience, default_alert="changed", options=options)
    #     print(jpush.received(["929251458"]))

