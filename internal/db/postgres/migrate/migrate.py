import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.absolute()))  # 添加backend项目根路径
from internal.db.postgres.workflows.repo import PaymentWorkflow
from internal.db.postgres.workflows.tokenization import MintWorkflow

from peewee_migrate import Router

from internal.db.postgres.common.accounts import Accounts, Addresses, Balances
from internal.db.postgres.common.workflow import WorkflowConfig, WorkflowStatusHistory, WorkflowCateConfig
from internal.db.postgres.base.base_models import db
from internal.db.postgres.migrate.migrate_patch import patch_pg_migrate_sql
from utils.logger import setup_log
from configurations import config

logger = setup_log("migrate")


def auto_migrate():
    """
    数据库迁移注意事项：
        [1.表中无数据]: 可以随便添加字段
        [2.表中有数据]:
            [注意]：新增非空限制属性时，如果表中本身有数据，则必须给默认值，不给默认值是矛盾的，且无法操作成功
        [综上]：添加非空限制的字段时，表中有数据，必须有默认值！！！！！！！！！！！！！！！！！！！！！！！
        已支持大部分场景, 其余几乎不会操作到的情况, 待接力...
    :return:
    """
    try:
        patch_pg_migrate_sql()
        db.connect()
        schema = config.get("database", "schema")
        if not db.execute_sql(
                f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema}';").fetchone():
            db.execute_sql(f"create schema {schema};")
        db.execute_sql(f"set search_path={schema};")
        if sys.argv[-1] == "drop":
            db.drop_tables(
                [Accounts, Addresses, Balances, WorkflowCateConfig, WorkflowConfig,
                 WorkflowStatusHistory, PaymentWorkflow, MintWorkflow])

            db.execute_sql(f"drop table if exists {schema}.migratehistory;")
            db.commit()
        router = Router(db, ignore='basemodel', schema=schema)
        logger.info("Generate migration file.")
        router.create(
            auto=[Accounts, Addresses, Balances, WorkflowCateConfig, WorkflowConfig,
                  WorkflowStatusHistory, PaymentWorkflow, MintWorkflow])
        logger.info("Create table structure.")
        router.run()
        db.close()
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    auto_migrate()
