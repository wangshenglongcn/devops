import paramiko
from db import HostDB, HostStatusDB
from encrypt import PasswordCipher


# -------------------
# Host连接、操作类
# -------------------
class Linux:
    def __init__(self, ip: str, user: str, password: str, timeout: int = 30):
        """通过ip、user、password、timeout初始化一个linux连接"""
        self._ip = ip
        self._user = user
        self._password = password
        self._timeout = timeout
        self._client = None

    def exec_command(self, cmd: str) -> str:
        """执行linux命令"""
        env = {"TERM": "xterm"}
        stdin, stdout, stderr = self._client.exec_command(cmd, environment=env)
        out = stdout.read().decode()
        err = stderr.read().decode()
        if err:
            raise Exception(f"Error on {self._ip}:", err)

        return out

    def get_cpu(self, cmd=""):
        pass

    def get_mem(self):
        pass

    def get_disk(self):
        pass

    def get_status(self):
        pass

    def start(self) -> None:
        """初始化linux机器连接"""
        if self._client:
            return

        # 初始化连接
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connect_args = {
            "hostname": self._ip,
            "username": self._user,
            "password": self._password,
            "timeout": self._timeout,
        }
        # 真正连接
        self._client.connect(**connect_args)
        if not self._client:
            raise Exception(f"{self._ip}初始化连接失败")

        print(f"Connected to {self._ip}")

    def stop(self) -> None:
        """关闭linux机器连接"""
        if self._client:
            self._client.close()
            self._client = None
            print(f"Disconnected from {self._ip}")

    # 通过配置__enter__/__exit__来实现上下文管理器, start/end也可以保证可以显示初始化或者销毁
    # 配置初始化时的操作，__enter__为了实现with语句
    # with Linux(**) as linux, linux指向__enter__函数返回的对象
    def __enter__(self):
        self.start()
        return self

    # 配置销毁时的动作, 4个参数是必需的，分别对应：异常类型、异常实例、traceback对象（堆栈信息）
    # 若正常退出则额外的3个参数均为None
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


# -------------------
# 主函数
# -------------------
def main():
    cmds = ["uptime", "df -h", "free -h"]

    password_cipher = PasswordCipher()
    with HostStatusDB() as host_status:
        with HostDB() as conn:
            for host in conn.query_all():
                password = password_cipher.decrypt(host.password)
                with Linux(host.ip, host.user, password) as linux:
                    cpu = linux.get_cpu()
                    mem = linux.get_mem()
                    disk = linux.get_disk()
                    status = linux.get_status()
                    host_status.insert(host.ip, cpu, mem, disk, status)


if __name__ == "__main__":
    main()
