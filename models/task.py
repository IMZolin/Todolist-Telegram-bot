from datetime import datetime

from peewee import CharField, BooleanField, DateTimeField, ForeignKeyField, DateField, TimeField, \
    AutoField

from . import User
from .base import BaseModel


class Task(BaseModel):
    id = AutoField(primary_key=True)
    author = ForeignKeyField(User, backref='tasks')
    text = CharField(default=None)
    date = DateField(formats='%d-%m-%Y', null=True)
    time = TimeField(formats='%H:%M:%S', null=True)
    is_done = BooleanField(default=False, null=True)
    periodicity = CharField(default=None, null=True)
    created_at = DateTimeField(default=lambda: datetime.utcnow())

    def __repr__(self) -> str:
        return f'<Task {self.text}>'

    class Meta:
        table_name = 'tasks'
