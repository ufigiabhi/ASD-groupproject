import hashlib
from datetime import datetime
from backend.database.db import get_connection


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class UserService:
    def authenticate(self, username: str, password: str):
        """
        Returns the user dict on success, or None on failure.
        Also updates last_login timestamp.
        """
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM users WHERE username = %s AND is_active = TRUE",
            (username,)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and user["password_hash"] == _hash(password):
            self._update_last_login(user["id"])
            return user
        return None

    def _update_last_login(self, user_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET last_login = %s WHERE id = %s",
            (datetime.now(), user_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    def get_all_users(self):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT id, username, role, full_name, email, phone, location, is_active, created_at "
            "FROM users ORDER BY role, full_name"
        )
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def create_user(self, username, password, role, full_name, email, phone=None, location=None):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO users
               (username, password_hash, role, full_name, email, phone, location)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (username, _hash(password), role, full_name, email, phone, location)
        )
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return new_id

    def deactivate_user(self, user_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET is_active = FALSE WHERE id = %s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()

    def reset_password(self, user_id: int, new_password: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (_hash(new_password), user_id)
        )
        conn.commit()
        cur.close()
        conn.close()
