from datetime import datetime
import hashlib


class User:
    def __init__(self, user_id: str, username: str, password: str):
        self.user_id = user_id
        self.username = username
        self.password_hash = self._hash_password(password)
        self.last_login_date = None

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def login(self, password: str) -> bool:
        if self.verify_password(password):
            self.last_login_date = datetime.now()
            return True
        return False
