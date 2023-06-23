import os
from datetime import datetime

from peewee import ModelUpdate, FieldAccessor
from playhouse.postgres_ext import SqliteDatabase, Model, DateTimeField, BooleanField, JSONField

from configurations import config
from internal.db.postgres.base.base_db import RetryPostgresqlDatabase

if config.get('database', 'port') == "5432":
    db = RetryPostgresqlDatabase.get_db_instance(database=config.get('database', 'name'),
                                                 host=config.get('database', 'host'),
                                                 port=config.get('database', 'port'),
                                                 user=config.get('database', 'user'),
                                                 password=config.get('database', 'pass'),
                                                 autorollback=True)
else:
    db = SqliteDatabase(os.getcwd() + '\\asx.db')


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.utcnow, verbose_name='created_at')
    last_updated = DateTimeField(default=datetime.utcnow, verbose_name='last_updated')
    is_deleted = BooleanField(default=False, verbose_name='is_deleted')
    extra_data = JSONField(null=True)

    class Meta:
        database = db
        schema = config.get("database", "schema")

    @classmethod
    def class_name(cls):
        return cls

    @classmethod
    def update(cls, __data=None, **update):
        update_time = datetime.utcnow()
        if __data:
            __data["last_updated"] = update_time
        if update:
            update["last_updated"] = update_time
        return ModelUpdate(cls, cls._normalize_data(__data, update))

    def to_json_default(self, model):
        fields = []
        for key, val in model.__dict__.items():
            if isinstance(val, FieldAccessor):
                fields.append(key)
        data = {}
        for k in fields:
            try:
                data[k] = getattr(self, k)
            except AttributeError:
                data[k] = ""
        return data

    def to_json(self):
        return self.to_json_default(self.class_name())
