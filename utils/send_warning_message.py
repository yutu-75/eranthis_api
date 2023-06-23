from utils.logger import setup_log

logger = setup_log()


def send_warning_message():
    # todo 消息写队列
    logger.exception(f"Greater than the maximum number of retries")
