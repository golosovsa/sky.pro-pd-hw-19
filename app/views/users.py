from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.user import UserSchema
from app.implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_movies = user_service.get_all()
        res = UserSchema(many=True).dump(all_movies)
        return res, 200

    def post(self):
        req_json = request.json
        movie = user_service.create(req_json)
        return "", 201, {"location": f"/users/{movie.id}"}


@user_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        data = user_service().dump(user)
        return data, 200

    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204

    def delete(self, bid):
        user_service.delete(bid)
        return "", 204
