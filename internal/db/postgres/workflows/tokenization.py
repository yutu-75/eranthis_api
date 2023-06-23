from peewee import ModelInsert
from playhouse.postgres_ext import *

from internal.db.postgres.base.base_models import BaseModel, db


class MintWorkflow(BaseModel):
    workflow_id = CharField(help_text="uuid unique identification", max_length=128, null=False)
    sender = CharField(help_text="Sender user of synfini", max_length=128, null=False)
    receiver = CharField(help_text="Receiver user of rba", max_length=128, null=False)
    amount = CharField(max_length=128, null=False)
    asset_name = CharField(max_length=128, null=False)
    workflow_status = IntegerField(help_text="workflow状态", null=False, default=0)
    event_cate = CharField(max_length=128, null=False)
    is_now = BooleanField(default=True)

    class Meta:
        table_name = "mint_workflow"

    @classmethod
    def insert(cls, __data=None, **insert):
        workflow_id = ""
        if __data:
            workflow_id = __data.get("workflow_id")
        if insert:
            workflow_id = insert.get("workflow_id")
        if workflow_id:
            with db.atomic():
                MintWorkflow.update({"is_now": False}).where(MintWorkflow.workflow_id == workflow_id,
                                                             MintWorkflow.is_now == True).execute()
                return ModelInsert(cls, cls._normalize_data(__data, insert))
        else:
            return ModelInsert(cls, cls._normalize_data(__data, insert))

    def to_json(self):
        res = super().to_json()
        return dict(asset=res["asset_name"], amount=res["amount"], sender=res["sender"], created_at=res["created_at"],
                    last_updated=res["last_updated"])
