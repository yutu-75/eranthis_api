from importlib import import_module
from flask import Blueprint

from gateway.config import CONFIG, APPS_BLUEPRINT_PATH


def init_blueprint(app, socketio):
    """自动注册蓝图"""
    api_version = CONFIG.get('api_version', 'v1')
    house_name = CONFIG['asx']['house_name']
    api = Blueprint('api', __name__, url_prefix=f"/{house_name}/{api_version}")

    for blueprint in APPS_BLUEPRINT_PATH:

        blueprint_path_list = blueprint.rsplit(".", 1)
        blueprint_name = blueprint_path_list[1]
        blueprint_path = blueprint_path_list[0]

        if '_ws' in blueprint:
            # 加载蓝图内部的socket接口
            getattr(import_module(blueprint), "start_socketio")(socketio)
        else:
            # 加载蓝图内部的restful接口
            api.register_blueprint(getattr(import_module(blueprint_path), blueprint_name))

    app.register_blueprint(api)
