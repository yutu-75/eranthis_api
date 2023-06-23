from internal.db.mongo.mongo_api import get_mongo_client
from internal.db.postgres.common.workflow import WorkflowStatusHistory
from internal.db.redis.redis_queue import RedisQueue
from utils.date_time_utils import get_str_datetime


def publish_to_redis(data):
    queue = RedisQueue("queue_workflow_data")
    queue.put(data)


def add_workflow_log_to_mongo(data):
    # 推送到redis队列
    publish_to_redis(data)

    # 写入mongo
    mongo_client = get_mongo_client()
    col = mongo_client.col_workflow_log
    workflow = col.find_one({'workflow_id': data.get("workflow_id")})
    if workflow:

        is_exist = col.find_one({'workflow_id': data.get("workflow_id"), "logs.status": data.get("status")})
        if is_exist:
            col.update_one(
                {'workflow_id': data.get("workflow_id"),"logs.status": data.get("status")},
                {
                    '$push': {
                        'logs.$.data': f"{get_str_datetime()} - {data.get('message')}"

                    }
                }
            )
        else:
            col.update_one(
                {'workflow_id': data.get("workflow_id")},
                {
                    '$push': {
                        'logs':
                            {
                                "data": [
                                    f"{get_str_datetime()} - {data.get('message')}"
                                ],
                                "status": data.get('status'),
                                "ctime": get_str_datetime()
                            }


                    }
                }
            )

    else:
        col.insert_one({
            "workflow_id": data.get("workflow_id"),
            "workflow_name": data.get("workflow_name"),
            "logs": [
                {
                    "data": [
                        f"{get_str_datetime()} - {data.get('message')}"
                    ],
                    "status": data.get('status'),
                    "ctime": get_str_datetime()
                }
            ]
        })


def add_workflow_status_history(data):
    return WorkflowStatusHistory.insert(**data).execute()


if __name__ == '__main__':
    print(add_workflow_log_to_mongo({
        "workflow_id": "12345678",
        "workflow_name": "test",
        "message": "test3333333333333333",
        "status": 300,
    }))
