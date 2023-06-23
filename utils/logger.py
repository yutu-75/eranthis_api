"""
1、 config中增加log块， formatter； log_dir, level; backupCount
2、
    exception:
    error:
    warning:
    info: 关键进程日志
    debug: 开发调试日志
    notice: 最高级别的日志
"""
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def setup_log(name=None):
    # todo config 配置
    log_formatter = logging.Formatter(
        '%(asctime)s - [%(threadName)s] - %(name)s - %(levelname)s - %(filename)s[%(lineno)d] - %(funcName)s - %(message)s '
    )
    # file handler
    log_dir = Path(__file__).parent.parent.joinpath('logs')
    if not log_dir.is_dir():
        log_dir.mkdir()
    file_name = str(log_dir.joinpath(f"daily_log_{name}.log").absolute())
    print('__________________________')
    file_handler = TimedRotatingFileHandler(
        file_name, when='MIDNIGHT', backupCount=30, encoding='utf8')
    file_handler.setFormatter(log_formatter)

    # stream handler # todo if dev
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.NOTSET)

    g_logger = logging.getLogger(name)
    g_logger.setLevel(logging.DEBUG)

    if g_logger.handlers:
        g_logger.handlers = list()

    g_logger.addHandler(file_handler)
    g_logger.addHandler(stream_handler)
    # g_logger.debug()
    return g_logger
