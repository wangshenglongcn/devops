from peewee import CharField, FloatField, DateTimeField
import datetime
from db.models.base import BaseModel


class HostStatus(BaseModel):
    ip = CharField(max_length=50)
    cpu = FloatField()
    memory = FloatField()
    disk = FloatField()
    status = CharField()  # offline / online
    batch_id = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "host_status"
        indexes = (("ip", "created_at"), False)
