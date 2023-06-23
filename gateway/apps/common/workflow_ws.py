import datetime
from copy import copy
from threading import RLock

from flask_socketio import Namespace
from peewee import fn, Value

from gateway.config import CONFIG
from internal.db.mongo.mongo_api import get_mongo_client
from internal.db.postgres.common.workflow import WorkflowStatusHistory
from internal.db.postgres.workflows.repo import PaymentWorkflow
from internal.db.postgres.workflows.tokenization import MintWorkflow
from internal.db.redis.redis_queue import RedisQueue
from utils.consts import WORKFLOW_CATE_PAYMENT

house_name = CONFIG['asx']['house_name']
BroadcastSpace = f"/{house_name}/workflow"  # 广播消息   server主动推
queue = RedisQueue("queue_workflow_data")


class BaseNamespace(Namespace):
    """
    socketio基类
    """

    def __init__(self, *args, **kwargs):
        self.namespace = args[0]
        self.app = None
        self.thread = None  # 多连接单后台任务
        self.thread_lock = RLock()
        super(BaseNamespace, self).__init__(*args, **kwargs)

    def on_connect(self):
        pass


class BroadNews(BaseNamespace):
    """
    广播类
    """

    def __init__(self, *args, **kwargs):
        self.socket_io = copy(kwargs.get("socket_io"))
        kwargs.pop('socket_io')
        super(BroadNews, self).__init__(*args, **kwargs)
        self.connection_num = 1
        self.on_connect()

    def on_connect(self):
        super().on_connect()
        self.socket_io.logger.info("start send data!!!!")
        self.socket_io.emit('work_flow_log', {'data': get_history_workflow_data()}, namespace=self.namespace)
        with self.thread_lock:
            if self.thread is None:
                self.thread = self.socket_io.start_background_task(target=self.broad_work_flow_log)

    def on_disconnect(self):
        pass

    def broad_work_flow_log(self):
        while True:
            workflow_data = queue.get()
            self.socket_io.logger.debug(f"workflow_data>>>{workflow_data}")

            history_workflow_data = get_history_workflow_data()
            print(history_workflow_data)
            self.socket_io.emit(
                "work_flow_log",
                {'data': history_workflow_data if workflow_data else history_workflow_data},
                namespace=self.namespace)
            self.socket_io.sleep(50)


def start_socketio(socketio):
    broad_news = BroadNews(BroadcastSpace, socket_io=socketio)
    socketio.on_namespace(broad_news)


mongo_client = get_mongo_client()
col = mongo_client.col_workflow_log


def get_history_workflow_data():
    # 取的数据是否有时间或者条数限制?
    all_workflow = []

    workflow_status_history_models = WorkflowStatusHistory.select(

    ).order_by(
        - Value(WorkflowStatusHistory.created_at).alias("created_at"))

    for item in workflow_status_history_models:
        if item.workflow_id not in [i.workflow_id for i in all_workflow] and item.status_code < 10000:
            all_workflow.append(item)

    response_list = []
    for i in all_workflow:
        workflow_data = {}
        workflow_data['workflow_id'] = i.workflow_id
        workflow_data['workflow_type'] = i.workflow_name
        workflow_data['networks'] = i.networks
        workflow_data['status'] = "Success" if i.status_code < 50000 else "Failed"
        workflow_data['date'] = i.created_at.strftime('%Y-%m-%d %H:%M:%S')

        tb = PaymentWorkflow if i.workflow_name == WORKFLOW_CATE_PAYMENT else MintWorkflow
        row = tb.select().where(tb.workflow_id == i.workflow_id, tb.is_now == True)
        if row.first():
            row_data = row.first().to_json()
            row_data['created_at'] = row_data['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            row_data['last_updated'] = row_data['last_updated'].strftime('%Y-%m-%d %H:%M:%S')
            row_data['workflow_log'] = col.find_one({'workflow_id': i.workflow_id})['logs']
            workflow_data['workflow_data'] = row_data
            workflow_data['workflow_data']['networks'] = i.networks
            response_list.append(workflow_data)

    return response_list


if __name__ == '__main__':
    s_time = datetime.datetime.now()
    history_workflow_data1 = get_history_workflow_data()
    print(history_workflow_data1)
    print(datetime.datetime.now() - s_time)
