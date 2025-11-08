from peewee import CharField
from db.models.base import BaseModel


class Host(BaseModel):
    ip = CharField(max_length=50, unique=True)
    user = CharField(max_length=50)
    password = CharField(max_length=255)

    class Meta:
        table_name = "hosts"
