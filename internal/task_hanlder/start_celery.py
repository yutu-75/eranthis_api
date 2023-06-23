import os

if __name__ == '__main__':
    os.system("celery -A workflow.registry_tasks worker -l info -P gevent")

