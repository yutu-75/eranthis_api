import time
from functools import wraps

from utils.send_warning_message import send_warning_message


def retry_decorator(db_retry_max_times=0):
    def _retry_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for i in range(db_retry_max_times if db_retry_max_times else self.db_retry_max_times):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    self.logger.exception(e)
                    time.sleep(1)
            else:
                #发送告警信息
                send_warning_message()

        return wrapper

    return _retry_decorator
