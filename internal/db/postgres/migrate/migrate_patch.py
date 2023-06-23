from peewee import ForeignKeyField, SENTINEL, logger, __exception_wrapper__, Database
from playhouse.migrate import operation, SchemaMigrator


@operation
def add_column(self, table, column_name, field):
    is_foreign_key = isinstance(field, ForeignKeyField)
    if is_foreign_key and not field.rel_field:
        raise ValueError('Foreign keys must specify a `field`.')

    operations = [self.alter_add_column(table, column_name, field)]

    # In the event the field is *not* nullable, update with the default
    # value and set not null.
    if not field.null:
        operations.extend([
            self.apply_default(table, column_name, field),
            self.add_not_null(table, column_name)])

    if is_foreign_key and self.explicit_create_foreign_key:
        operations.append(
            self.add_foreign_key_constraint(
                table,
                column_name,
                field.rel_model._meta.table_name,
                field.rel_field.column_name,
                field.on_delete,
                field.on_update))

    if field.index or field.unique:
        using = getattr(field, 'index_type', None)
        operations.append(self.add_index(table, (column_name,),
                                         field.unique, using))

    return operations


def execute_sql(self, sql, params=None, commit=SENTINEL):
    logger.debug((sql, params))
    if commit is SENTINEL:
        if self.in_transaction():
            commit = False
        elif self.commit_select:
            commit = True
        else:
            commit = not sql[:6].lower().startswith('select')

    with __exception_wrapper__:
        cursor = self.cursor(commit)
        try:
            if "TYPE" in sql and "DEFAULT" in sql:
                tmp_sql, default = sql.split("TYPE DEFAULT")
                prefix_sql, field_type = tmp_sql.strip().rsplit(" ", 1)
                sql_1 = f"{prefix_sql} TYPE {field_type} using {prefix_sql.rsplit(' ')[-1]}::{field_type}"
                sql_2 = f"{prefix_sql} set DEFAULT {default}"
                cursor.execute(sql_1, params or ())
                cursor.execute(sql_2, params or ())
            else:
                cursor.execute(sql, params or ())

        except Exception as e:
            if self.autorollback and not self.in_transaction():
                self.rollback()
            raise
        else:
            if commit and not self.in_transaction():
                self.commit()
    return cursor


def patch_pg_migrate_sql():
    SchemaMigrator.add_column = add_column
    Database.execute_sql = execute_sql