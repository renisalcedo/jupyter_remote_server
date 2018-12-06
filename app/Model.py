from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()

class User(db.Model):
    """ Model for the user
    :type id: int
    :type username: str
    :type password: str
    :type job: str
    :type notebooks: [Notebook]
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    job = db.Column(db.String(250), nullable=True)
    notebooks = db.relationship('Notebook', backref='user', lazy=True)

class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(3))
    password = fields.String(required=True, validate=validate.Length(8))
    job = fields.String(validate=validate.Length(2))