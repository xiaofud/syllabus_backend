# coding=utf-8
__author__ = 'smallfly'

import json
from datetime import datetime

# {
#       "post_time": "2016-09-16 14:51:06",
#       "comments": [],
#       "id": 941,
#       "post_type": 0,
#       "thumb_ups": [],
#       "photo_list_json": null,
#       "description": "",
#       "content": "真的要补课吗",
#       "source": "iOS",
#       "user": {
#         "account": "16yqliu2",
#         "nickname": "文奇奇😛",
#         "id": 3192,
#         "image": "http://bmob-cdn-5361.b0.upaiyun.com/2016/09/10/8cc3a1fd8d3e4a73b7ae2feee457a49b.jpg"
#       }
#     }

def make_notice(content, source, account, nickname):
    photo_list_json = None
    description = ""
    post_type = 0
    thumb_ups = []
    comments = []
    id_ = 0
    user = {
        "account": account,
        "nickname": nickname,
        "id": 0,
        "image": None
    }
    post_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return{
          "post_time": post_time,
          "comments": comments,
          "id": id_,
          "post_type": post_type,
          "thumb_ups": thumb_ups,
          "photo_list_json": photo_list_json,
          "description": description,
          "content": content,
          "source": source,
          "user": user
    }

def main():
    lines = []
    print("input content, end by empty line: ")
    while True:
        line = input(">> ")
        if line:
            lines.append(line)
        else:
            break
    content = "\n".join(lines)
    source = input("source: ")
    account = input("account: ")
    nickname = input("nickname: ")
    notice = make_notice(content, source, account, nickname)
    print(notice)
    with open("notice.txt", "w") as f:
        json.dump(notice, f)


if __name__ == "__main__":
    main()