from backend.models.user import User


class AuthService:
    def __init__(self):
        self.users = {}

    def register_user(self, user: User) -> None:
        self.users[user.username] = user

    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if not user:
            return False
        return user.login(password)
