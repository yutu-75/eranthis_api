import grpc
import traceback


# from util import send_slack
# from utils.zc_exception import ZCException


class ErrorManager(object):

    def __init__(self, context):
        self.logger = context.logger
        self.request_attributes = [
            'user_id', 'tenant', 'asset_id', 'address', 'tag', 'customer_ref_id',
            'limit', 'page', 'term', 'yield_id', 'type', 'side', 'amount', 'vault_id',
            'external_wallet_id', 'values']

    def grpc_exception_handling(self, context, name, e, request):
        value_dic = self.parse_request(request)
        self.logger.exception(f"{name} failed e={repr(e.__str__())} values={value_dic}")

    def parse_request(self, request):
        value_dic = {}
        for i in self.request_attributes:
            if hasattr(request, i):
                value_dic[i] = getattr(request, i)

        return value_dic
