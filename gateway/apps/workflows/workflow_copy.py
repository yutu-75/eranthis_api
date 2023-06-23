import json
from datetime import datetime
from functools import reduce

from flask import Blueprint, request
from peewee import FieldAccessor, operator, fn

from gateway.logger import LogDecorator
from gateway.utils.params_check import verify_all_params_not_none, verify_params_exists, \
    verify_is_party_free_balance_enough
from internal.common.accounts.account_utils import get_house_address
from internal.common.gen_random_obj import get_new_uuid
from internal.db.mongo.mongo_api import get_mongo_client
from internal.db.postgres.api.payment import add_payment_workflow_to_db
from internal.db.postgres.api.tokenization import add_mint_workflow
from internal.db.postgres.common.workflow import WorkflowStatusHistory
from internal.db.postgres.workflows.repo import PaymentWorkflow
from internal.db.postgres.workflows.tokenization import MintWorkflow
from internal.workflows.common.workflow_log_utils import add_workflow_log_to_mongo
from internal.workflows.repo.contract_consts import PAYMENT_STATUS_WORKFLOW_TO_DB
from internal.workflows.tokenization.contract_consts import EVENT_FRONTEND, MINT_STATUS_WORKFLOW_TO_DB

from monitor.grpc_client import grpc_send_data
from utils.consts import *
from utils.date_time_utils import get_str_datetime
from utils.encrypt import keccak_256
from utils.error_code_msg import ParamsError

bp_workflow = Blueprint(
    'bp_workflow',
    __name__,
    url_prefix='/workflows'
)
mongo_client = get_mongo_client()
col = mongo_client.col_workflow_log


def create_workflow_payment(workflow_data):
    verify_all_params_not_none(workflow_data)
    verify_params_exists(
        workflow_data.keys(),
        ['receiver_address', 'receiver_party', 'bank_receiver_party', 'amount'])

    sender = get_house_address()
    workflow_data['sender_party'] = sender.get("synfini")
    if sender.get("address") == workflow_data.get("receiver_address"):
        raise Exception('can not pay to self')
    sender_balance = verify_is_party_free_balance_enough(
        workflow_data["sender_party"], int(workflow_data.get("amount")), workflow_data.get("asset"))

    preimage = get_new_uuid()
    event_data = {
        'workflow_id': get_new_uuid(),
        "sender_address": sender.get("rba"),
        "receiver_address": workflow_data.get("receiver_address"),
        "sender_party": workflow_data.get('sender_party'),
        # sub account 认证出来的 todo ，根据token解析到sub account，获取party_id
        "receiver_party": workflow_data.get("receiver_party"),
        "bank_receiver_party": workflow_data.get("bank_receiver_party"),
        "hash_lock": keccak_256(preimage),
        "preimage": preimage,
        "amount": workflow_data.get("amount"),
        "workflow_cate": WORKFLOW_CATE_PAYMENT,
        "balance_id": sender_balance["payload"]["id"],
        "htlc_hash": "",
        "txn_hash": "",
        "transfer_label": get_new_uuid(),
        "asset": workflow_data.get("asset"),
        'event': "create",
        "event_cate": FRONTEND_OPERATION

    }
    add_payment_workflow_to_db(event_data)
    add_workflow_log_to_mongo({
        "workflow_id": event_data.get("workflow_id"),
        "workflow_name": WORKFLOW_CATE_PAYMENT,
        "message": "frontend operation create payment",
        "status": PAYMENT_STATUS_WORKFLOW_TO_DB,
        "ctime": get_str_datetime()
    })

    grpc_responses = grpc_send_data(
        {
            'workflow_cate': WORKFLOW_CATE_PAYMENT,
            'event_cate': FRONTEND_OPERATION,
            'event_data': json.dumps(
                event_data
            )
        }
    )
    return str(grpc_responses)


def create_workflow_mint(workflow_data):
    verify_all_params_not_none(workflow_data)
    verify_params_exists(
        workflow_data.keys(),
        ['network', 'asset', 'amount']
    )

    sender = get_house_address().get(workflow_data.get("network"))
    event_data = {
        'workflow_id': get_new_uuid(),
        "sender": sender,
        "receiver": sender,
        "network": workflow_data.get("network"),
        "asset": workflow_data.get("asset"),
        "amount": workflow_data.get("amount"),
        "workflow_cate": WORKFLOW_CATE_MINT,
        'event': "create",
        "event_cate": EVENT_FRONTEND

    }
    add_mint_workflow(event_data)
    grpc_responses = grpc_send_data(
        {
            'workflow_cate': WORKFLOW_CATE_MINT,
            'event_cate': EVENT_FRONTEND,
            'event_data': json.dumps(event_data

                                     )
        }
    )
    return str(grpc_responses)


@bp_workflow.route("/workflow", methods=['POST'])
@LogDecorator()
def start_workflow():
    """
    开始工作流
    :workflow_name str  workflow任务名称
    :workflow_data dict 开启workflow任务需要的参数
    :return:
    """

    data = request.get_json()
    workflow_name = data.get("workflow_name")
    workflow_data = data.get("workflow_data")
    verify_all_params_not_none(data)
    if workflow_name == WORKFLOW_CATE_PAYMENT:
        return create_workflow_payment(workflow_data)
    elif workflow_name == WORKFLOW_CATE_MINT:
        return create_workflow_mint(workflow_data)

    return "no workflow"


@bp_workflow.route("/workflow", methods=['GET'])
@LogDecorator()
def get_workflows():
    """
    获取workflow数据的历史数据
    :status bool 如果为True查询的status数据 < 10000,False 则相反
    :page int   那一页的数据,为0或者不传则为全部数据
    :page int   一页有多少条数据
    :return:
    """
    data = dict(request.values.items())
    network = data.get("network")
    status = data.get("status")
    date = data.get("date")

    where_list = []

    if network:
        where_list.append(WorkflowStatusHistory.networks == network)

    if status:
        print([status])
        where_list.append(
            WorkflowStatusHistory.status_code < 10000
            if status == "Success" else
            WorkflowStatusHistory.status_code > 10000)

    if date:
        date = date.split(',')
        start_date = date[0],
        end_date = date[1]
        where_list.append(
            (start_date <= WorkflowStatusHistory.created_at) & (WorkflowStatusHistory.created_at <= end_date)
        )

    if where_list:
        workflow_status_history_models = WorkflowStatusHistory.select(
            WorkflowStatusHistory.workflow_id,
            WorkflowStatusHistory.workflow_name,
            WorkflowStatusHistory.networks,
            fn.MAX(WorkflowStatusHistory.status_code).alias("status_code"),
            fn.MAX(WorkflowStatusHistory.created_at).alias("created_at")
        ).where(reduce(operator.and_, where_list)).group_by(
            WorkflowStatusHistory.workflow_id,
            WorkflowStatusHistory.workflow_name,
            WorkflowStatusHistory.networks,
        )

    else:
        workflow_status_history_models = WorkflowStatusHistory.select(
            WorkflowStatusHistory.workflow_id,
            WorkflowStatusHistory.workflow_name,
            WorkflowStatusHistory.networks,
            fn.MAX(WorkflowStatusHistory.status_code).alias("status_code"),
            fn.MAX(WorkflowStatusHistory.created_at).alias("created_at")
        ).group_by(
            WorkflowStatusHistory.workflow_id,
            WorkflowStatusHistory.workflow_name,
            WorkflowStatusHistory.networks,

        )
    if data.get("page"):
        workflow_status_history_models.paginate(data.get("page"), data.get("page_size", 10))

    response_list = []

    for i in workflow_status_history_models:
        workflow_data = {}
        workflow_data['workflow_id'] = i.workflow_id
        workflow_data['workflow_type'] = i.workflow_name
        workflow_data['networks'] = i.networks
        workflow_data['status'] = "Success" if i.status_code else "Failed"
        workflow_data['date'] = i.created_at.strftime('%Y-%m-%d %H:%M:%S')
        response_list.append(workflow_data)
    return response_list


@bp_workflow.route("/workflow/<workflow_id>", methods=['GET'])
@LogDecorator()
def get_workflow_data(workflow_id):
    """
    根据workflow_id获取workflow数据
    :workflow_id int workflow_id
    :return:
    """
    if workflow_id:
        res = WorkflowStatusHistory.select().where(WorkflowStatusHistory.workflow_id == workflow_id).first()

        tb = PaymentWorkflow if res.workflow_name == WORKFLOW_CATE_PAYMENT else MintWorkflow
        response_list = []
        row = tb.select().where(tb.workflow_id == workflow_id).first()

        row_data = row.to_json()
        row_data['created_at'] = row_data['created_at'].strftime('%Y-%m-%d %H:%M:%S')

        row_data['workflow_log'] = col.find_one({'workflow_id': workflow_id})['logs']
        response_list.append(row_data)
    else:
        return []
    return response_list


@bp_workflow.route("/confirm", methods=['POST'])
@LogDecorator()
def confirm():
    data = request.get_json()
    verify_all_params_not_none(data)
    verify_params_exists(data.keys(), ['hash_lock'])

    hash_lock = data.get("hash_lock")
    workflow_id = data.get("workflow_id")
    workflow = PaymentWorkflow.select().where(PaymentWorkflow.hash_lock == hash_lock).first()
    if not workflow:
        raise ParamsError.PARAMS_NOT_VALID.format(f'hash_lock error')
    grpc_send_data(
        {
            'workflow_cate': WORKFLOW_CATE_PAYMENT,
            'event_cate': FRONTEND_OPERATION,
            'event_data': json.dumps(
                {
                    "hash_lock": hash_lock,
                    'workflow_id': workflow_id,
                    "event": "confirm"
                }
            )
        }
    )

    return "ok"
