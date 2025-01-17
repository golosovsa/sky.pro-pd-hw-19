from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.director import DirectorSchema
from app.implemented import director_service
from app.service.auth import auth_required, admin_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        director = director_service.create(req_json)
        return "", 201, {"location": f"/directors/{director.id}"}


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        director = director_service.get_one(rid)
        data = DirectorSchema().dump(director)
        return data, 200

    @admin_required
    def put(self, rid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = rid
        director_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, rid):
        director_service.delete(rid)
        return "", 204
