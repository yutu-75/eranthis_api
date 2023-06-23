from internal.db.postgres.workflows.tokenization import MintWorkflow
from internal.workflows.tokenization.contract_consts import MINT_STATUS_WORKFLOW_CREATED


def add_mint_workflow(data):

    MintWorkflow(
        workflow_id=data.get("workflow_id"),
        sender=data.get("sender"),
        receiver=data.get("receiver"),
        networks=[data.get("network")],
        amount=data.get("amount"),
        asset_name=data.get("asset"),
        event_cate=data.get("event_cate"),
    ).save()


def get_mint_workflow(symbol):
    return MintWorkflow.select().where(
        MintWorkflow.asset_name == symbol,
        MintWorkflow.is_now == True,
        MintWorkflow.workflow_status == MINT_STATUS_WORKFLOW_CREATED
    ).first()


def update_mint_workflow(data):
    data.workflow_status = data.get("workflow_status")
    data.id = None
    data.save()
