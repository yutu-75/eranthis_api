from configurations import config

#########################################################################################
# synfini
#########################################################################################
PKG_ID = config.get('daml', "pkg_id")

# daml合约

REPO_SUB_WORK_FLOW_TEMPLATE = f"{PKG_ID}:RepoSubWorkflow:RepoSubWorkflow"

#########################################################################################
# rba
#########################################################################################
RBA_HTLC_EVENTS_STR = 'rba_htlc_events'
NEW_HEAD_EVENTS_STR = 'new_head_events'
HTLC_CREATED_STR = 'HTLCCreated'
HTLC_WITHDRAWN_STR = 'HTLCWithdrawn'
HTLC_REFUNDED_STR = 'HTLCRefunded'

EXPIRATION_TIME_LOCK = 100

# monitor event => topic
# w3.w3.sha3(text="HTLCCreated(address,address,address,bytes32,uint256,uint256)")
CREATE_HTLC = "0x0041d34812126cf9edc2958769f466a8d1c1285a37035306e94558425a7b6411"
# w3.w3.sha3(text="HTLCWithdrawn(address,string)")
WITHDRAW_HTLC = "0xfbdee7263b1c6634346bd369fc07ddb9b2b69f90c1605eb4abfeddee447f8598"
# w3.w3.sha3(text="HTLCRefunded(address)")
REFUND_HTLC = "0x4329f239422f89684f9412393325839870726ad2ef495a319ef674dac19c129c"

RBA_EVENTS = {
    RBA_HTLC_EVENTS_STR: {HTLC_CREATED_STR: CREATE_HTLC, HTLC_WITHDRAWN_STR: WITHDRAW_HTLC,
                          HTLC_REFUNDED_STR: REFUND_HTLC}
}

PAYMENT_STATUS_WORKFLOW_TO_DB = 0
PAYMENT_STATUS_WORKFLOW_CREATED = 100
PAYMENT_STATUS_WORKFLOW_UPDATE_HASH = 200
PAYMENT_STATUS_WORKFLOW_CONFIRMED = 300
PAYMENT_STATUS_PREIMAGE_UPLOADED = 400
PAYMENT_STATUS_ONE_OF_ENDPOINTS_COMPLETED = 500
PAYMENT_STATUS_BOSS_ENDPOINTS_COMPLETED = 600
PAYMENT_STATUS_WORKFLOW_COMPLETED = 10000
PAYMENT_STATUS_HTLC_ROLLBACK = 20000
PAYMENT_STATUS_WORKFLOW_ROLLBACK = 30000
