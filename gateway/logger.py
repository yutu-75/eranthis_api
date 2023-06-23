import functools
import json
from datetime import datetime
from bson import json_util
from flask import jsonify

from utils.logger import setup_log
from utils.zc_exception import ZCException

logger = setup_log('gateway')


class LogDecorator:
    def __init__(self):
        self.logger = logger

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            try:
                s_time = datetime.now()
                self.logger.debug(f"{fn.__name__}.input: {args} {kwargs}")
                result = fn(*args, **kwargs)
                self.logger.debug(f"{fn.__name__}.output: {result}")
                self.logger.debug(f"{fn.__name__}.runtime: {datetime.now()-s_time}")
                result = json.loads(json_util.dumps(result))
                response = jsonify(dict(status="success", result=result if result else []))

                return response
            except ZCException as zc_ex:
                self.logger.exception(f"{fn.__name__}.Exception: {str(zc_ex.error_message)}")
                response = jsonify(dict(status="failed", msg=str(zc_ex.error_message), code=zc_ex.error_code))
                response.status_code = zc_ex.error_code
                return response
            except Exception as ex:
                self.logger.exception(f"{fn.__name__}.Exception: {str(ex)}")
                response = jsonify(dict(status="failed", msg=str(ex), code=9999))
                response.status_code = 9999
                return response

        decorated.__name__ = fn.__name__
        return decorated
