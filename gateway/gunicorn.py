# gunicorn configuration file

import multiprocessing
import os
from gateway.config import CONFIG


print(f"Starting gunicorn with {CONFIG['host']}:{CONFIG['port']}")

# config
bind = f"{CONFIG['host']}:{CONFIG['port']}"  # 绑定 ip + 端口
workers = multiprocessing.cpu_count() * 2 + 1  # 进程数 = cup数量 * 2 + 1
threads = multiprocessing.cpu_count() * 2  # 线程数 = cup数量 * 2
timeout = 120  # 超时时间
keepalive = 2  # 保持连接时间
preload_app = True  # 预加载资源
backlog = 2048  # 等待队列最大长度,超过这个长度的链接将被拒绝连接
worker_class = "gevent"
worker_connections = 1200  # worker 最大客户客户端并发数量, 对使用线程和协程的 worker 有影响
proc_name = 'gunicorn'  # 进程名称
pidfile = 'gunicorn.pid'  # 进程pid记录文件
loglevel = 'info'  # 日志等级
accesslog = 'logs/access.log'  # 访问日志
access_log_format = '%(h)s %(t)s %(U)s %(q)s'  # 访问记录格式
# h	远程地址
# l	"-"
# u	用户名
# t	时间
# r	状态行, 如: GET /test HTTP/1.1
# m	请求方法
# U	没有查询字符串的URL
# q	查询字符串
# H	协议
# s	状态码
# B	response长度
# b	response长度(CLF格式)
# f	参考
# a	用户代理
# T	请求时间, 单位为s
# D	请求时间, 单位为ms
# p	进程id
# {Header}i	请求头
# {Header}o	相应头
# {Variable}e	环境变量
errorlog = 'logs/error.log'  # 错误日志
