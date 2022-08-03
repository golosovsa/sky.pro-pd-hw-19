import base64
import hashlib
import hmac

from flask_restx import abort

from app.dao.user import UserDAO
from app.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_data):
        username = user_data.get("username")
        password = user_data.get("password")
        role = user_data.get("role")

        if not username or not password or not role:
            abort(400)

        user_data = {
            "username": username,
            "password": self.get_hash(password),
            "role": role,
        }

        return self.dao.create(user_data)

    def update(self, user_data):
        self.dao.update(user_data)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    @staticmethod
    def get_hash(password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    @staticmethod
    def compare_passwords(hashed_password: str, open_password):
        return hmac.compare_digest(
            base64.b64decode(hashed_password.encode("utf-8") + b'=='),
            base64.b64decode(UserService.get_hash(password=open_password).encode("utf-8") + b'==')
        )
