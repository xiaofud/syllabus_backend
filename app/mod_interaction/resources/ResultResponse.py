# coding=utf-8
__author__ = 'smallfly'

"""
采用统一的返回格式
"""
import json

class ResultResponse(object):
    """
    采用统一的格式对返回结果编码
    {
        "code": int # 用一个整数表明这次请求的状态
        "message": str 描述code的含义
        "data": JSON_OBJECT 实际返回的数据
    }
    """
    def __init__(self):
        self._code = None
        self._message = None
        self._data = None

    @staticmethod
    def makeResponse(code, message, data):
        response = ResultResponse()
        response.code = code
        response.message = message
        response.data = data
        return response

    def to_json(self):
        response = {
            "code": self._code,
            "message": self._message,
            "data": self.data
        }
        return json.dumps(response)

    def get_code(self):
        return self._code

    def set_code(self, code):
        if isinstance(code, int):
            self._code = code
        else:
            raise ValueError("code must be integer")

    def get_message(self):
        return self._message

    def set_message(self, message):
        if isinstance(message, str):
            self._message = message
        else:
            raise ValueError("message must be str")

    def get_data(self):
        return self._data

    def set_data(self, obj):
        self._data = obj

    def __repr__(self):
        response = {
            "code": self._code,
            "message": self._message,
            "data": self.data
        }
        return repr(response)

    code = property(get_code, set_code)
    message = property(get_message, set_message)
    data = property(get_data, set_data)


if __name__ == "__main__":
    syllabus = {
        "w1": "math",
        "w2": "programming"
    }
    response = ResultResponse.makeResponse(0, "succeed", syllabus)
    print(response.to_json())