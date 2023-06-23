import threading
import time


class SafeStopThread(threading.Thread):
    def __init__(self, loop_sleep_time=0, logger=None):
        self.logger = logger
        self.stop_event = threading.Event()  # 创建一个事件管理标志，该标志（event）默认为False
        self.loop_sleep_time = loop_sleep_time
        super().__init__()

    def stop(self):
        self.stop_event.set()  # 将event的标志设置为True，调用wait方法的所有线程将被唤醒

    def stopped(self):
        return self.stop_event.is_set()  # 判断event的标志是否为True

    def run_once(self):

        raise NotImplementedError

    def run(self) -> None:
        while not self.stopped():
            try:
                self.run_once()
            except Exception as e:
                self.logger.exception(e)
            finally:
                if self.loop_sleep_time:
                    time.sleep(self.loop_sleep_time)
