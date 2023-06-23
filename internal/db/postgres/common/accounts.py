from peewee import ForeignKeyField, CharField, BooleanField, IntegerField

from internal.db.postgres.base.base_models import BaseModel


class Accounts(BaseModel):
    """
    bank 级别对外的（机构）
    """
    name = CharField(max_length=64, unique=True, null=False)
    is_me = BooleanField(help_text="是否为自己", default=False)

    class Meta:
        table_name = "accounts"


class Addresses(BaseModel):
    """
    bank 级别对外的（机构）
    """
    account = ForeignKeyField(Accounts, help_text="acconut_id", null=False)
    network = CharField(help_text="交易链", max_length=128, null=False)
    address = CharField(help_text="交易地址", max_length=128, null=False)
    private_key = CharField(help_text="交易私钥", max_length=128, default="", null=True)
    is_house = BooleanField(help_text="是否为主用户", default=True)

    class Meta:
        table_name = "addresses"


class Balances(BaseModel):
    address = ForeignKeyField(Addresses)
    asset = CharField(max_length=128, null=False)
    network = CharField(max_length=128, null=False)
    lock = IntegerField(default=0)
    free = IntegerField(default=0)
    total = IntegerField(default=0)

    class Meta:
        table_name = "balances"
