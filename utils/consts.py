from configurations import config

#########################################################################################
# synfini
#########################################################################################
PKG_ID = config.get('daml', "pkg_id")

# daml合约
REGISTRY_TEMPLATE = f"{PKG_ID}:Registry:Registry"
BALANCE_TEMPLATE = f"{PKG_ID}:Balance:Balance"

# daml 合约 操作方法
METHODS_DAML_CREATE_AND_EXERCISE = 'create-and-exercise'
METHODS_DAML_CREATE = 'create'
METHODS_DAML_EXERCISE = 'exercise'
METHODS_DAML_QUERY = 'query'
METHODS_DAML_FETCH = 'fetch'

#########################################################################################

# workflow
#########################################################################################
SYNFINI_WORKFLOW_EVENTS_STR = "synfini_workflow_events"

WORKFLOW_CATE_PAYMENT = "bank_to_bank_payment"
WORKFLOW_CATE_MINT = "workflow_mint"
FRONTEND_OPERATION = "frontend_operation"

#########################################################################################
# restful
#########################################################################################
REQUEST_OK = 200
REQUEST_INVALID_AUTH = 401
REQUEST_NOT_FOUND = 404
REQUEST_TOO_MANY_REQUESTS = 429
REQUEST_BAD_GATEWAY = 502
REQUEST_UNAVAILABLE = 503
REQUEST_GATEWAY_TIMEOUT = 504

#########################################################################################
# redis
#########################################################################################

QUEUE_NAME_SCHEDULER = 'queue_name_scheduler'

#########################################################################################
# common
#########################################################################################

# 交易(HTLC)状态
ACTIVE = 'Active'
INACTIVE = 'Inactive'
COMPLETED = 'Completed'

# 币种
USDZ = "USDZ"

# 交易链
RBA_NETWORK = "rba"
SYNFINI_NETWORK = "synfini"

#########################################################################################
# celery
#########################################################################################


RESULT_STATUS_STARTED = 'STARTED'
RESULT_STATUS_SUCCESS = 'SUCCESS'
RESULT_STATUS_PENDING = 'PENDING'
RESULT_STATUS_FAILURE = 'FAILURE'
RESULT_STATUS_REVOKED = 'REVOKED'
RESULT_STATUS_RETRY = 'RETRY'
