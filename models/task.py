from datetime import datetime

from peewee import BigIntegerField, CharField, BooleanField, DateTimeField, ForeignKeyField

from . import User
from .base import BaseModel


class Task(BaseModel):
    id = BigIntegerField(primary_key=True)
    author = ForeignKeyField(User)
    text = CharField(default=None)
    time = DateTimeField(formats='%d-%m-%Y %S:%M:%H', null=True)
    is_done = BooleanField(default=False, null=True)
    is_periodic = BooleanField(default=False, null=True)
    created_at = DateTimeField(default=lambda: datetime.utcnow())

    def __repr__(self) -> str:
        return f'<Task {self.text}>'

    class Meta:
        table_name = 'tasks'