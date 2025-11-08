from peewee import IntegrityError
from db.base import DB
from db.models.host import Host


class HostDB(DB):
    model = Host

    def insert(self, ip: str, user: str, password: str) -> None:
        try:
            self.model.create(ip=ip, user=user, password=password)
        except IntegrityError:
            print(f"[Duplicate] {ip} skipped")
        except Exception as e:
            print(f"[ERROR] Insert failed for {ip}: {e}")
