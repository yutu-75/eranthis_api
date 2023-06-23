import decimal
import json



def verify_all_params_not_none(params):

    for key, value in params.items():
        if not value:
            raise Exception(f'params[{key}] is none')
    return True


def verify_params_exists(params, must_contains_list=[]):

    for item in must_contains_list:
        if item not in params:
            raise Exception(f'params[{item}] is needed')
    return True


def is_json(test_str):
    try:
        json_object = json.loads(test_str)  # 通过json.loads判断
    except Exception as e:
        return False
    return True
