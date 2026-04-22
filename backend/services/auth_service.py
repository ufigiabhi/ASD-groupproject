#================================================================
# Module:      UFCF8S-30-2 Advanced Software Development
# Project:     PAMS - Paragon Apartment Management System
# Author(s):    Esila Keskin 
# Student ID(s):  24064432  
# Description: Auth service - authentication wrapper used in model-layer unit tests
#================================================================

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
