from functools import reduce
from peewee import operator, Value, fn
from flask import Blueprint, request

from gateway.logger import LogDecorator
from gateway.utils.params_check import verify_all_params_not_none, verify_params_exists
from internal.common.accounts.account_utils import get_house_address
from internal.db.postgres.common.accounts import Balances, Addresses, Accounts

bp_account = Blueprint(
    'bp_account',
    __name__,
    url_prefix='/accounts'
)


@bp_account.route("/option", methods=['GET'])
@LogDecorator()
def get_Asset_network_option():
    """
    获取当前用户的所有的asset,network
    :return:
    """
    address_list = list(get_house_address().values())
    address_id_list = [i.id for i in Addresses.select().where(Addresses.address.in_(address_list))]
    asset_models = Balances.select(Balances.asset).where(Balances.address.in_(address_id_list)).group_by(Balances.asset)

    asset_list = [i.asset for i in asset_models]
    network_list = [
        i.network
        for i in Addresses.select(Addresses.network)
        .where(Addresses.address.in_(address_list)).group_by(Addresses.network)
    ]

    return {
        "asset": asset_list,
        "network": network_list
    }


@bp_account.route("/balances", methods=['GET'])
@LogDecorator()
def get_accounts_balances():
    """
    根据network以及asset查询账户资产
    :asset str      币种
    :network str    链(Synfini or Goerli)
    :return:
    """
    data = dict(request.values.items())

    where_list = []
    if data.get('network'):
        where_list.append(Balances.network == data.get('network'))
    if data.get('asset'):
        where_list.append(Balances.asset == data.get('asset'))
    if where_list:
        result_models = Balances.select().where(reduce(operator.and_, where_list))
    else:
        result_models = Balances.select()

    total = result_models.count()

    if data.get("page"):
        result_models = result_models.paginate(int(data.get("page")), int(data.get("page_size", 100)))

    response_list = {
        "data":
            [{
                "asset": i.asset,
                "balances": {
                    "lock": i.lock,
                    "free": i.free,
                    "total": i.total,
                },
                "network": i.network
            } for i in result_models],
        "total": total
    }

    return response_list


@bp_account.route("/add", methods=['POST'])
@LogDecorator()
def add_account_and_address():
    """
    增加account用户
    :name str           account 用户
    :address str        地址
    :network str        链(Synfini or Goerli)
    :return:
    """
    data = request.get_json()
    accounts_models = Accounts.select().where(Accounts.name == data.get("name")).first()

    if accounts_models:
        address = Addresses(account=accounts_models.id, address=data.get("address"), network=data.get('network'), )
        address.save()
    else:
        account = Accounts(name=data.get("name"))
        account.save()

        address = Addresses(account=account, address=data.get("address"), network=data.get('network'), )
        address.save()

    return "ok"


@bp_account.route("/edit", methods=['POST'])
@LogDecorator()
def edit_account_and_address():
    """
    修改address地址
    :name str           account 用户
    :address str        地址
    :network str        链(Synfini or Goerli)
    :return:
    """
    data = request.get_json()
    account_models = Accounts.select().where(Accounts.name == data.get("name")).first()

    if not Addresses.update(address=data.get("address")).where(
            Addresses.account == account_models.id,
            Addresses.network == data.get('network')
    ).execute():
        raise Exception("Users without this chain")

    return "ok"


@bp_account.route("/names", methods=['GET'])
@LogDecorator()
def get_accounts_names():
    """
    获取Accounts表里所有用户名(name)
    :return:
    """
    result_models = Accounts.select()
    response_list = [i.name for i in result_models]
    return response_list


@bp_account.route("/", methods=['GET'])
@LogDecorator()
def get_receivers():
    # house_account = get_house_account()
    result = Addresses.select().join(Accounts).where(Accounts.is_me == False)
    response_dict = {}
    for item in result:
        if response_dict.get(item.account.name):
            response_dict[item.account.name].append({"network": item.network, "address": item.address})
        else:
            response_dict[item.account.name] = [{"network": item.network, "address": item.address}]

    response_list = [{"account_name": i, "address_list": response_dict[i]} for i in response_dict]

    return response_list
