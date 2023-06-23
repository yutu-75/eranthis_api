import decimal

from external.synfini_gateway.apis.common_apis.balance import get_owner_balance


def verify_is_party_free_balance_enough(party, amount, asset):
    sender_balance = get_owner_balance({"id": {"asset": asset}}, party)
    if not sender_balance or decimal.Decimal(sender_balance[0]["payload"]["free"]) < int(amount):
        raise Exception(f'{party} balance not enough')
    return sender_balance[0]
