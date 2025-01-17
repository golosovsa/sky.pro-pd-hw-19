"""
    User model
"""
from marshmallow import Schema, fields

from app.setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()
