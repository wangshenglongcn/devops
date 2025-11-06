from peewee import *
from encrypt import PasswordCipher
import config
from typing import List, Type
import datetime

# -------------------
# 数据库配置
# -------------------
db = MySQLDatabase("demo", **config.db_config, host="localhost", port=3306)


# -------------------
# 模型定义
# -------------------
class Base(Model):
    class Meta:
        database = db


class Host(Base):
    """主机表模型"""

    ip = CharField(max_length=50, unique=True)
    user = CharField(max_length=50)
    password = TextField()

    class Meta:
        table_name = "hosts"


class HostStatus(Base):
    """主机状态模型"""

    ip = CharField(max_length=50)
    cpu = FloatField()
    memory = FloatField()
    disk = FloatField()
    status = CharField()  # offline or online
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "host_status"
        # 联合索引用以加速查询，如select().where(ip == "").order_by(created_at.desc())
        # 在表上创建一个组合索引（联合索引），字段是 ip + created_at
        # False 表示这个索引 不是唯一索引
        indexes = (("ip", "created_at"), False)


# -------------------
# 数据库操作类
# -------------------
class DB:
    """数据库类，支持上下文管理"""

    model: Type[Model] = None

    def __init__(self):
        self._connected = False

    def start(self) -> None:
        if self._connected:
            return

        try:
            db.connect(reuse_if_open=True)
            db.create_tables([self.model])
            self._connected = True
            print("Connected to MySQL database")
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise

    def stop(self) -> None:
        if self._connected:
            db.close()
            self._connected = False
            print("Disconnected to database")

    def query_all(self) -> List[Model]:
        """查询所有记录"""
        if not self.model:
            raise RuntimeError("No model defined for DB subclass")
        return list(self.model.select())

    # 上下文管理器
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()


class HostDB(DB):
    model = Host

    def insert(self, ip: str, user: str, password: str) -> None:
        """插入主机记录"""
        try:
            self.model.create(ip=ip, user=user, password=password)
        except IntegrityError:
            print(f"Duplicate entry skipped: {ip}")
        except Exception as e:
            print(f"Insert failed for {ip}: {e}")


class HostStatusDB(DB):
    model = HostStatus

    def insert(
        self,
        ip: str,
        cpu: float,
        mem: float,
        disk: float,
        status: str,
    ) -> None:
        """插入主机状态记录"""
        try:
            self.model.create(ip=ip, cpu=cpu, mem=mem, disk=disk, status=status)
        except IntegrityError:
            print(f"Duplicate entry skipped: {ip}")
        except Exception as e:
            print(f"Insert failed for {ip}: {e}")


# -------------------
# 测试运行
# -------------------
if __name__ == "__main__":
    # 写入Host数据库测试
    password_cipher = PasswordCipher()
    with HostDB() as conn:
        for host in config.hosts:
            conn.insert(
                host["ip"], host["user"], password_cipher.encrypt(host["password"])
            )

        for host in conn.query_all():
            print(host.ip, host.user, host.password)
