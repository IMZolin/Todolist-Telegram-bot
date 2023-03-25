"""
Peewee migrations -- 003_Task.py.
Some examples (model - class or model name)::
    > Model = migrator.orm['model_name']            # Return model in current state by name
    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
"""
import datetime
import datetime as dt
import json

import peewee as pw
from decimal import ROUND_HALF_EVEN

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class BaseModel(pw.Model):
        id = pw.AutoField()

        class Meta:
            table_name = "basemodel"

    @migrator.create_model
    class User(pw.Model):
        id = pw.BigIntegerField(primary_key=True)
        name = pw.CharField(max_length=255)
        username = pw.CharField(max_length=255, null=True)
        language = pw.CharField(constraints=[SQL("DEFAULT 'en'")], default='en', max_length=255)
        is_admin = pw.BooleanField(constraints=[SQL("DEFAULT False")], default=False)
        created_at = pw.DateTimeField()

        class Meta:
            table_name = "users"

    class TimeDeltaField(pw.Field):
        db_field = 'blob'

        def db_value(self, value):
            if value is not None:
                return json.dumps({
                    'days': value.days,
                    'seconds': value.seconds,
                    'microseconds': value.microseconds,
                }).encode('utf-8')
            return None

        def python_value(self, value):
            if value is not None:
                td_dict = json.loads(value.decode('utf-8'))
                return datetime.timedelta(
                    days=td_dict['days'],
                    seconds=td_dict['seconds'],
                    microseconds=td_dict['microseconds']
                )
            return None

    @migrator.create_model
    class Task(BaseModel):
        id = pw.AutoField(primary_key=True)
        author = pw.ForeignKeyField(User, backref='tasks')
        text = pw.CharField(default=None)
        done_date = pw.DateField(formats='%d.%m.%Y', null=True)
        date = pw.DateField(default=None, formats='%d.%m.%Y', null=True)
        time = pw.TimeField(formats='%H:%M:%S', null=True)
        is_done = pw.BooleanField(default=False, null=True)
        periodicity = pw_pext.IntervalField(default=None, null=True)
        created_at = pw.DateTimeField(default=lambda: datetime.datetime.utcnow())

        class Meta:
            table_name = 'tasks'



def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    # migrator.remove_model('users')

    migrator.remove_model('basemodel')
