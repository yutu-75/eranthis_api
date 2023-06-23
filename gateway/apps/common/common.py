from flask import Blueprint, request
from gateway.logger import LogDecorator
from internal.db.postgres.common.workflow import WorkflowConfig, WorkflowCateConfig

bp_common = Blueprint(
    'bp_common',
    __name__,
    url_prefix='/common'
)


@bp_common.route("/workflows", methods=['GET'])
@LogDecorator()
def get_all_cate_workflows():
    """
    获取workflow数据
    :return:
    """

    result_models = WorkflowConfig.select(WorkflowConfig.name, WorkflowConfig.cate).join(WorkflowCateConfig).distinct()
    response_dict = {}

    for i in result_models:
        if response_dict.get(i.cate.name):
            response_dict[i.cate.name].append(i.name)
        else:
            response_dict[i.cate.name] = [i.name]

    response_list = [{"cate": i, "name_list": response_dict[i]} for i in response_dict]

    return response_list
