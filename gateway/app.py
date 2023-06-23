import sys
from pathlib import Path
from flask import Flask
from flask_socketio import SocketIO
from gevent import monkey
from gevent.pywsgi import WSGIServer

sys.path.append(str(Path(__file__).parent.parent.absolute()))  # 加载backend项目根路径
sys.path.append(str(Path(__file__).parent.parent.absolute() / "scheduler/proto"))
from gateway.utils.blueprint_utils import init_blueprint
from gateway.middleware.hooks import set_app_hook
from utils.logger import setup_log
from gateway.config import CONFIG

api_version = CONFIG.get('api_version', 'v1')
house_name = CONFIG['asx']['house_name']

app = Flask(__name__)
app.json.ensure_ascii = False

logger = setup_log('app')

# # 日志初始化
# app.logger = logger

# 注册socket
socketio = SocketIO()
socketio.init_app(app, async_mode="gevent", cors_allowed_origins="*", debug=True)
socketio.logger = logger


# 注册蓝图
init_blueprint(app, socketio)


if __name__ == "__main__":
    print(app.url_map)
    from flask_cors import CORS
    CORS(app, supports_credentials=True)

    # app.run(host='0.0.0.0', port=CONFIG.get("port"), debug=True, use_reloader=False)
    WSGIServer(('0.0.0.0', 8888), app, log=logger).serve_forever()
    # socketio.run(app, host="127.0.0.1", port=int(CONFIG.get("port")), debug=True)
