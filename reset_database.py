# coding=utf-8
__author__ = 'smallfly'

from app.mod_interaction.models import *
# 建立一些测试用途的数据
def generate_test_data():
    # 一些测试数据

    import json
    photo_list = {
        "photo_list":[
            {
                "size_big": "https://xiaofud.me/img/746ff7890c10e100.jpg",
                "size_small": "https://xiaofud.me/img/746ff7890c10e100.jpg"
            },
            {
                "size_big": "https://xiaofud.me/img/img0082.jpg",
                "size_small": "https://xiaofud.me/img/img0082.jpg"
            }
        ]
    }
    photo_list_json = json.dumps(photo_list, ensure_ascii=True)

    xiaofud = {
        "account": "14xfdeng",
        "nickname": "晓拂",
        # "birthday": "1995-12-23",
        "gender": 1,
        "profile": "hello world"
    }

    user = User(**xiaofud)
    db.session.add(user)
    db.session.commit()

    post_info = {
            "post_type": 1,
            "uid": user.id,
            # "title": "this is title",
            "content": "this is content" * 100,
            "description": "this is description",
            "photo_list_json": photo_list_json
    }

    post = Post(**post_info)
    db.session.add(post)
    db.session.commit()


    for i in range(5):

        user_info = {
            "account": "14xfdeng " + str(i),
            "nickname": "xiaofud" + str(i),
            "birthday": "1995-12-23",
            "gender": 1,
            "profile": "hello world"
        }
        user = User(**user_info)

        db.session.add(user)
        db.session.commit()

        post_info = {
            "post_type": 1,
            "uid": user.id,
            # "title": "this is title",
            "content": "this is content %d\n" % i  ,
            "description": "this is description",
            "photo_list_json": photo_list_json
        }

        post = Post(**post_info)

        db.session.add(post)
        db.session.commit()

        comment_info = {
            "post_id": post.id,
            "uid": user.id,
            "comment": "hello world" * 8
        }
        comment = Comment(**comment_info)

        db.session.add(comment)
        db.session.commit()

        like_info = {
            "uid": user.id,
            "post_id": post.id
        }

        like = ThumbUp(**like_info)

        db.session.add(like)
        db.session.commit()

# print("called")
# db.drop_all()
# db.create_all()
# generate_test_data()

if __name__ == "__main__":
    db.drop_all()
    db.create_all()