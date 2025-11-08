from peewee import MySQLDatabase, Model
from settings.config import DB_CONFIG
from typing import Type, List

# 数据库连接
db = MySQLDatabase("demo", **DB_CONFIG, port=3306)


class DB:
    """数据库操作基类，支持上下文管理器"""

    model: Type[Model] = None

    def __init__(self):
        self._connected = False

    def start(self) -> None:
        if self._connected:
            return
        if not self.model:
            raise RuntimeError("No model defined for DB subclass")
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
            print("Disconnected from database")

    def query_all(self) -> List[Model]:
        return list(self.model.select())

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()


# -------------------
# 测试运行
# -------------------
if __name__ == "__main__":
    # 写入Host数据库测试
    pass
    # password_cipher = PasswordCipher()
    # with HostDB() as conn:
    #     for host in config.hosts:
    #         conn.insert(
    #             host["ip"], host["user"], password_cipher.encrypt(host["password"])
    #         )

    #     for host in conn.query_all():
    #         print(host.ip, host.user, host.password)
