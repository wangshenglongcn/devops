import paramiko
from db.repositories.host_db import HostDB
from db.repositories.host_status_db import HostStatusDB
from encrypt import PasswordCipher
import socket
from typing import Tuple
import re
import time


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
        self.alive = False

        self.alive = self._check_reachable()

    def _check_reachable(self) -> bool:
        """尝试TCP能否连接通"""
        try:
            socket.create_connection((self._ip, 22), timeout=self._timeout).close()
            return True
        except Exception:
            return False

    def exec_command(self, cmd: str) -> Tuple[str, int]:
        """执行linux命令"""
        env = {"TERM": "xterm"}
        stdin, stdout, stderr = self._client.exec_command(cmd, environment=env)
        out = stdout.read().decode()
        err = stderr.read().decode()
        return_code = 0
        if err:
            return_code = 1
            print(f"[ERROR] {self._ip} when exec {cmd}: {err}")

        return (out, return_code)

    def get_cpu(self, cmd="top -b -n 1 | grep 'Cpu(s)'") -> float:
        out, return_code = self.exec_command(cmd)
        if return_code:
            return 0.0

        # 提取 "id" 前的数字, 即空闲率，cpu使用率 = 100 - 空闲率
        match = re.search(r"(\d+\.\d+)\s+id", out)
        if match:
            idle = float(match.group(1))
            usage = round(100 - idle, 2)
            print(f"[INFO] CPU使用率: {usage}%")
            return usage
        else:
            print(f"[ERROR] 执行 {cmd} 未找到CPU空闲率")
            return 0.0

    def get_mem(self, cmd="free | awk '/Mem/{printf(\"%.2f\", ($3/$2)*100)}'"):
        out, return_code = self.exec_command(cmd)
        if return_code:
            return 0.0

        usage = float(out)
        print(f"[INFO] MEM使用率: {usage}%")
        return usage

    def get_disk(self, cmd="df -h --total | grep total | awk '{print $5}' | tr -d %"):
        out, return_code = self.exec_command(cmd)
        if return_code:
            return 0.0

        usage = float(out)
        print(f"[INFO] DISK使用率: {usage}%")
        return usage

    def start(self) -> None:
        """初始化linux机器连接"""
        if not self.alive:
            print(f"[WARNING] {self._ip} 无法连接")
            return

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
        try:
            self._client.connect(**connect_args)
            print(f"[INFO] Connected to {self._ip}")
        except Exception:
            self._client = None
            self.alive = False
            print(f"[ERROR] {self._ip}初始化连接失败")

    def stop(self) -> None:
        """关闭linux机器连接"""
        if self._client:
            self._client.close()
            self._client = None
            print(f"[INFO] Disconnected from {self._ip}")

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


def scheduler():
    password_cipher = PasswordCipher()
    batch_id = str(int(time.time()))
    with HostStatusDB() as host_status:
        with HostDB() as conn:
            for host in conn.query_all():
                password = password_cipher.decrypt(host.password)
                with Linux(host.ip, host.user, password) as linux:
                    if not linux.alive:
                        host_status.insert(host.ip, 0.0, 0.0, 0.0, "offline", batch_id)
                    else:
                        cpu = linux.get_cpu()
                        mem = linux.get_mem()
                        disk = linux.get_disk()
                        host_status.insert(host.ip, cpu, mem, disk, "online", batch_id)


# -------------------
# 主函数
# -------------------
def main():
    while True:
        print("执行任务中……")
        scheduler()
        time.sleep(60)  # 每 60 秒执行一次


if __name__ == "__main__":
    main()
    # scheduler()
