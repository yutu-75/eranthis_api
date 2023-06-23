from internal.db.redis.redis_queue import RedisQueue
from utils.consts import QUEUE_NAME_SCHEDULER
from utils.logger import setup_log
from utils.safe_stop_thread import SafeStopThread


class MessageConsumer(SafeStopThread):

    def __init__(self):
        self.logger = setup_log('send_message')
        self.logger.info(f">>>>>> {self.__class__.__name__}  Launched >>>>>>")
        SafeStopThread.__init__(self, logger=self.logger)
        self.queue = RedisQueue(QUEUE_NAME_SCHEDULER)

    def send_message(self, message):
        self.logger.info(f"Need to send a message. message :{message}")

    def run_once(self):
        result = self.queue.get_with_block_mode(is_dict_mode=True)
        if result:
            self.send_message(result)
