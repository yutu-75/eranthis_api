from utils.zc_exception import ZCException


class AuthError:
    """
    当前系统认证或权限相关错误
    error_code : [10000 , 20000)
    """
    USER_NOT_FOUND = ZCException(error_code=10001, error_message="The user [{}] is not found")
    PASSWORD_INCORRECT = ZCException(error_code=10002, error_message="Password is not correct")
    NO_PERMISSION = ZCException(error_code=10003, error_message="You do not have permission")
    USER_OR_PASSWORD_NOT_FOUND = ZCException(error_code=10004, error_message="user or password is empty")
    NEED_LOGIN = ZCException(error_code=10005, error_message="not login")



class ParamsError:
    """
    参数相关错误
    error_code : [20000 , 30000)
    """
    PARAMS_TOO_LONG = ZCException(error_code=20001, error_message="The param [{}] is too long")
    PARAMS_NOT_VALID = ZCException(error_code=20002, error_message="The param [{}] is not valid")
    PARAMS_NOT_VALID_MSG = ZCException(error_code=20003, error_message="{}")


class SecurityLimitError:
    """
    安全限制相关报错
    error_code : [30000 , 40000)
    """
    ACCESS_COUNT_ERROR = ZCException(error_code=30001,
                                     error_message="Requests are too frequent. Try again in {} seconds")


class CodeError:
    """
    代码相关报错
    error_code : [40000 , 50000)
    """
    CALC_ERROR = ZCException(error_code=40001, error_message="calc format error")


class OperationError:
    """
    业务流程相关错误
    error_code : [50000 , 60000)
    """
    SOMETHING_WRONG = ZCException(error_code=50001, error_message="something wrong")
    ACCESS_INVALID = ZCException(error_code=50002, error_message="{}")
    NOT_FOUND = ZCException(error_code=50003, error_message="{} not found")
    DATA_ERROR = ZCException(error_code=50004, error_message="data error: {}")


class DamlApiError:
    """
    访问daml节点返回错误
    error_code : [60000 , 70000)
    """
    DAML_ACCESS_ERROR = ZCException(error_code=60001, error_message="{}")
    GET_TOKEN_ERROR = ZCException(error_code=60002, error_message="get token error")


class OsApiError:
    """
    系统相关
    error_code : [70000 , 80000)
    """
    FILE_NOT_EXISTS = ZCException(error_code=70001, error_message="{} is not exists")
