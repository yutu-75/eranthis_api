from configurations import config


CONFIG = {
    'api_version': config.get('gateway', 'api_version'),
    'host': config.get('gateway', 'host'),
    'port': config.get('gateway', 'port'),
    'grpc': {
        'host': config.get('grpc', 'host'),
        'port': config.get('grpc', 'port'),
    },
    'asx': {
        'house_name': config.get('asx', 'house_name'),
    }
}

APPS_BLUEPRINT_PATH = [
    # "gateway.apps.common.account.bp_account",
    "gateway.apps.books.bp_books",
    # "gateway.apps.common.workflow_ws",
    # "gateway.apps.workflows.workflow.bp_workflow",
    # "gateway.apps.common.common.bp_common",
]
