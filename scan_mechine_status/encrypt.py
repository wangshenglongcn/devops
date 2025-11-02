from cryptography.fernet import Fernet
import os


key_file = "secret.key"


# -------------------
# 数据加解密类
# -------------------
class PasswordCipher:
    """管理 Fernet 密钥，并提供加解密功能"""

    def __init__(self, key_file: str = "secret.key"):
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        self.fernet = Fernet(self.key)

    def _load_or_generate_key(self) -> bytes:
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            print(f"Generated new key and saved to {self.key_file}")

        return key

    def encrypt(self, data: str) -> str:
        """加密字符串，返回可存储的字符串"""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted: str) -> str:
        """解密字符串"""
        return self.fernet.decrypt(encrypted.encode()).decode()


if __name__ == "__main__":
    password_cipher = PasswordCipher()
