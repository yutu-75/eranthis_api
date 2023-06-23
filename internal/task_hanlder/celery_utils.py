import sys
from pathlib import Path
from celery.result import AsyncResult

sys.path.append(str(Path(__file__).parent.parent.absolute()))
from workflow.app import celery_app


def get_task_result(task_id):
    res = AsyncResult(task_id, app=celery_app)
    return {
        'status': res.status,
        'result': res.result
    }


def delete_task(task_id):
    c_task = AsyncResult(task_id)
    c_task.forget()


if __name__ == '__main__':
    print(get_task_result("ddd"))
    print(delete_task("ddd"))


