from configurations import config

#########################################################################################
# synfini
#########################################################################################
PKG_ID = config.get('daml', "pkg_id")

# daml合约
TOKENIZATION_WORK_FLOW_TEMPLATE = f"{PKG_ID}:TokenizationWorkflow:TokenizationWorkflow"
TOKENIZATION_ASSET_DEPOSIT_TEMPLATE = f"{PKG_ID}:TokenizationAssetDeposit:TokenizationAssetDeposit"

EVENT_FRONTEND = 'event_fronted'
EVENT_ETH = 'event_eth'
EVENT_SYNFINI = 'event_synfini'
EVENT_MINT_ASSET = 'mint_asset'

MINT_STATUS_WORKFLOW_TO_DB = 0
MINT_STATUS_WORKFLOW_CREATED = 100
MINT_STATUS_WORKFLOW_COMPLETED = 10000
MINT_STATUS_WORKFLOW_ROLLBACK = 30000