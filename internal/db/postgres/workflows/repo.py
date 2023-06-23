from peewee import ModelInsert
from playhouse.postgres_ext import JSONField, CharField, IntegerField, BooleanField

from internal.db.postgres.base.base_models import BaseModel, db


class PaymentWorkflow(BaseModel):
    workflow_id = CharField(help_text="uuid unique identification", max_length=128, null=False)
    sender_party = CharField(help_text="Sender user of synfini", max_length=128, null=False)
    sender_address = CharField(help_text="Sender user of rba", max_length=128, null=False)
    receiver_party = CharField(help_text="Receiver user of synfini", max_length=128, null=False)
    receiver_address = CharField(help_text="Receiver user of rba", max_length=128, null=False)
    hash_lock = CharField(max_length=128, null=False)
    time_lock = IntegerField(default=0)
    preimage = CharField(max_length=128, default=None, null=True)
    amount = CharField(max_length=128, null=False)
    asset = CharField(max_length=128, null=False)
    workflow_status = IntegerField(help_text="workflow状态", null=False, default=0)
    created_at_synfini = CharField(max_length=128, null=True)
    htlc_hash = CharField(max_length=256, null=True)
    completed_set = JSONField()
    event_cate = CharField(max_length=128, null=False)
    confirm = BooleanField(default=False)
    is_now = BooleanField(default=True)

    class Meta:
        table_name = "payment_workflow"
        indexes = (
            (('workflow_status', 'workflow_id', 'hash_lock', 'preimage'), True),
        )

    @classmethod
    def insert(cls, __data=None, **insert):
        hash_lock = ""
        if __data:
            hash_lock = __data.get("hash_lock")
        if insert:
            hash_lock = insert.get("hash_lock")
        if hash_lock:
            with db.atomic():
                PaymentWorkflow.update({"is_now": False}).where(PaymentWorkflow.hash_lock == hash_lock,
                                                                PaymentWorkflow.is_now == True).execute()
                return ModelInsert(cls, cls._normalize_data(__data, insert))
        else:
            return ModelInsert(cls, cls._normalize_data(__data, insert))

    def to_json(self):
        res = super().to_json()
        return dict(asset=res["asset"], amount=res["amount"], sender=res["sender_party"], created_at=res["created_at"],
                    last_updated=res["last_updated"], hash_lock=res["hash_lock"])
