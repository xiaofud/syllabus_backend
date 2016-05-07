# coding=utf-8
__author__ = 'smallfly'

import json
import os

FILENAME = "config.txt"
CUR_DIR = os.path.dirname(__file__)
FILENAME = os.path.join(CUR_DIR, FILENAME)

def input_key():
    app_key = input("app key: ")
    master_key = input("master: key")
    config = {
        "app_key": app_key,
        "master_key": master_key
    }
    with open(FILENAME, "w") as f:
        json.dump(config, f)

def read_key():
    if not os.path.exists(FILENAME):
        return None
    with open(FILENAME) as f:
        obj = json.load(f)
        return obj["app_key"], obj["master_key"]

if __name__ == "__main__":
    input_key()
    print(read_key())