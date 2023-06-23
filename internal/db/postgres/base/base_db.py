from peewee import PostgresqlDatabase, InterfaceError, OperationalError, SENTINEL
from playhouse.shortcuts import ReconnectMixin


class RetryPostgresqlDatabase(ReconnectMixin, PostgresqlDatabase):
    _instance = {}

    def __init__(self, *args, **kwargs):
        super(RetryPostgresqlDatabase, self).__init__(*args, **kwargs)
        self._reconnect_errors[InterfaceError] = ["connection already closed unexpectedly", "connection already closed"]
        self._reconnect_errors[OperationalError] = ["could not connect to server",
                                                    "server closed the connection unexpectedly"]

    @staticmethod
    def get_db_instance(*args, **kwargs):
        if not RetryPostgresqlDatabase._instance.get(kwargs.get('database')):
            RetryPostgresqlDatabase._instance[kwargs.get('database')] = RetryPostgresqlDatabase(*args, **kwargs)
        return RetryPostgresqlDatabase._instance[kwargs.get('database')]

    def execute_sql(self, sql, params=None, commit=SENTINEL):
        try:
            return super(ReconnectMixin, self).execute_sql(sql, params, commit)
        except Exception as exc:
            exc_class = type(exc)
            if exc_class not in self._reconnect_errors:
                raise exc

            exc_repr = str(exc).lower()
            for err_fragment in self._reconnect_errors[exc_class]:
                if err_fragment in exc_repr:
                    break
            else:
                raise exc

            if not self.is_connection_usable():
                self.close()
                self.connect()

            return super(ReconnectMixin, self).execute_sql(sql, params, commit)
