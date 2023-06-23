from utils.logger import setup_log

logger = setup_log('workflow_queue')


def workflow_log(log_msg):
    logger.info(log_msg)
