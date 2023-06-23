from internal.db.postgres.common.accounts import Addresses, Accounts


def get_house_address():
    house_accounts = Addresses.select().join(Accounts).where(Accounts.is_me == True, Addresses.is_house == True)

    return {item.network: item.address for item in house_accounts}


def get_account_by_party(party):
    pass


def get_current_workflow_party(workflow):
    pass
