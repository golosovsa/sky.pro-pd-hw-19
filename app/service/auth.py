"""
    Authenticate service class
"""
import calendar
import datetime

import jwt
from flask_restx import abort

from app.constants import JWT_SECRET, JWT_ALGORITHM
from app.dao.model.user import User
from app.service.user import UserService


class AuthService:
    def __init__(self, user_service):
        self.user_service: UserService = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        if not username or not (password or is_refresh):
            abort(401)

        user: User = self.user_service.get_by_username(username)
        if user is None:
            abort(401)

        if not is_refresh and not self.user_service.compare_passwords(
                user.password, password
        ):
            abort(400)

        data = dict(username=user.username, role=user.role)

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return dict(access_token=access_token, refresh_token=refresh_token)

    def approve_refresh_token(self, refresh_token):

        data = {}

        try:
            data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.exceptions.PyJWTError:
            abort(401)

        username = data.get("username", None)

        return self.generate_tokens(username, None, True)
