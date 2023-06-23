from flask import request, jsonify

from internal.common.error_code.error_code_msg import ParamsError


def check_params():
    if request.method.upper() in ('POST', 'PUT'):
        json_data = request.get_json()
        if json_data:
            if isinstance(json_data, dict):
                for key, value in json_data.items():
                    if len(str(key)) > 256 or len(str(value)) > 2048000:
                        return jsonify(
                            dict(status="failed", msg=ParamsError.PARAMS_TOO_LONG.error_message.format(str(key)),
                                 code=ParamsError.PARAMS_TOO_LONG.error_code))
