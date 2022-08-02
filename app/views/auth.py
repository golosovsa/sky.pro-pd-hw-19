from flask import request
from flask_restx import Namespace, Resource

from app.implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        user_data = request.json
        username = user_data.get("username", None)
        password = user_data.get("password", None)

        return auth_service.generate_tokens(username, password)

    def put(self):
        refresh_token = request.form.get("refresh_token", None)

        return auth_service.approve_refresh_token(refresh_token)
