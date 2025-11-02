from peewee import *
from encrypt import PasswordCipher
import config
from typing import List

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


# -------------------
# 数据库操作类
# -------------------
class DB:
    """数据库类，支持上下文管理"""

    def __init__(self):
        self._connected = False

    def start(self) -> None:
        if self._connected:
            return

        try:
            db.connect(reuse_if_open=True)
            db.create_tables([Host])
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

    def insert(self, ip: str, user: str, password: str) -> None:
        """插入主机记录"""
        try:
            Host.create(ip=ip, user=user, password=password)
        except IntegrityError:
            print(f"Duplicate entry skipped: {ip}")
        except Exception as e:
            print(f"Insert failed for {ip}")

    def query_all(self) -> List[Host]:
        """查询所有主机"""
        return list(Host.select())

    # 上下文管理器
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()


# -------------------
# 测试运行
# -------------------
if __name__ == "__main__":
    password_cipher = PasswordCipher()
    with DB() as conn:
        for host in config.hosts:
            conn.insert(
                host["ip"], host["user"], password_cipher.encrypt(host["password"])
            )

        for host in conn.query_all():
            print(host.ip, host.user, host.password)
