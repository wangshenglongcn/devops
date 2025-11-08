from db.base import Model, db


class BaseModel(Model):
    class Meta:
        database = db
