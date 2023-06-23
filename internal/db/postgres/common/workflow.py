from playhouse.postgres_ext import CharField, IntegerField, BooleanField, ForeignKeyField, JSONField, BinaryJSONField

from internal.db.postgres.base.base_models import BaseModel
from internal.db.postgres.workflows.repo import PaymentWorkflow
from internal.db.postgres.workflows.tokenization import MintWorkflow
from utils.consts import WORKFLOW_CATE_PAYMENT


class WorkflowCateConfig(BaseModel):
    name = CharField(help_text="workflow name", max_length=128, null=False, unique=True)
    sort = IntegerField(default=0)
    is_config = BooleanField(default=True)

    class Meta:
        table_name = "workflow_cate_config"


class WorkflowConfig(BaseModel):
    name = CharField(help_text="workflow name", max_length=128, null=False, unique=True)
    cate = ForeignKeyField(WorkflowCateConfig)
    sort = IntegerField(default=0)
    is_config = BooleanField(default=True)

    class Meta:
        table_name = "workflow_config"


class WorkflowStatusHistory(BaseModel):
    workflow_name = CharField(help_text="workflow name", max_length=128, null=False)
    workflow_id = CharField(help_text="workflow id", max_length=128, null=False)
    networks = BinaryJSONField()
    status_code = IntegerField(default=0)
    status_message = CharField(max_length=128, null=False)

    class Meta:
        table_name = "workflow_status_history"

    def work_flow_to_json(self):
        res = self.to_json()
        tb = PaymentWorkflow if self.workflow_name == WORKFLOW_CATE_PAYMENT else MintWorkflow
        res["workflow_content"] = [row.to_json() for row in tb.select().where(tb.workflow_id == self.workflow_id)]
        return res
