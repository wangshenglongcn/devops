from db.base import DB
from db.models.host_status import HostStatus
from typing import List
import datetime


class HostStatusDB(DB):
    model = HostStatus

    def insert(
        self,
        ip: str,
        cpu: float,
        memory: float,
        disk: float,
        status: str,
        batch_id: str,
    ) -> None:
        try:
            self.model.create(
                ip=ip,
                cpu=cpu,
                memory=memory,
                disk=disk,
                status=status,
                batch_id=batch_id,
                created_at=datetime.datetime.now(),
            )
        except Exception as e:
            print(f"[ERROR] Insert failed for {ip}: {e}")

    def get_latest_batch_id(self) -> str:
        latest = (
            self.model.select(self.model.batch_id)
            .order_by(self.model.created_at.desc())
            .limit(1)
            .scalar()
        )
        return latest

    def query_status(self) -> List[HostStatus]:
        batch_id = self.get_latest_batch_id()
        if not batch_id:
            return []
        return list(self.model.select().where(self.model.batch_id == batch_id))
