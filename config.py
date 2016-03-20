# coding=utf-8
import os, json

config = dict()

# Statement for enabling the development environment
config["DEBUG"] = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
config["BASE_DIR"] = BASE_DIR


# private settings
with open("config.conf") as f:
    config.update(json.load(f))

