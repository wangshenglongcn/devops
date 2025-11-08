from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
from db.repositories.host_status_db import HostStatusDB


app = FastAPI()


# -------------------
# 定义pydantic模型
# -------------------
class HostStatusSchema(BaseModel):
    ip: str
    cpu: float
    memory: float
    disk: float
    status: str
    created_at: datetime
    batch_id: str


# -------------------
# 定义/对应的返回数据
# -------------------
@app.get("/", response_model=List[HostStatusSchema])
def read_root():
    with HostStatusDB() as conn:
        return conn.query_status()
