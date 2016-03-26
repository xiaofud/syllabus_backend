# coding=utf-8
__author__ = 'smallfly'

from flask_restful import Resource
from app.mod_interaction.resources import helpers

# 检测版本升级
class VersionResource(Resource):
    """
        用于控制app升级的api
    """
    VERSION_FILE = "version.txt"

    # 返回最新的版本号 versionCode 整型
    def get(self):
        version_obj = helpers.load_version()
        if version_obj is None:
            return {"error": "not found"}, 404
        return dict(versionCode=version_obj['versionCode'], versionName=version_obj['versionName'],
                        versionDescription=version_obj['description'], versionDate=version_obj['versionDate'],
                       versionReleaser=version_obj['versionReleaser'], download_address=version_obj['download_address'],
                       apk_file_name=version_obj['apk_file_name'])
