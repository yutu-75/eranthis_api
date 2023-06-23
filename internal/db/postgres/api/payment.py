from internal.db.postgres.workflows.repo import PaymentWorkflow


def add_payment_workflow_to_db(data):
    data = {
        "workflow_id": data.get("workflow_id"),
        "sender_party": data.get("sender_party"),
        "receiver_party": data.get("receiver_party"),
        "sender_address": data.get("sender_address"),
        "receiver_address": data.get("receiver_address"),
        "hash_lock": data.get("hash_lock"),
        "completed_set": {},
        "preimage": data.get("preimage"),
        "amount": data.get("amount"),
        "asset": data.get("asset"),
        "workflow_cate": data.get("workflow_cate"),
        "event_cate": data.get("event_cate"),
    }
    PaymentWorkflow(**data).save()
