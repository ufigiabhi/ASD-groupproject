from backend.models.user import User
from backend.services.auth_service import AuthService

auth = AuthService()

user = User("U001", "esila", "password123")
auth.register_user(user)

print(auth.login("esila", "password123"))  # True
print(auth.login("esila", "wrongpass"))    # False
