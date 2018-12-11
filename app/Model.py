from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()

class UserModel(db.Model):
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
    # Relation with the notebooks
    notebooks = db.relationship("NotebookModel", backref='users')
 
    def __init__(self, username, password, job):
        self.username = username
        self.password = password
        self.job = job
        

class UserSchema(ma.Schema):
    """ Schema for the user
    :type id: Int
    :type username: Str
    :type password: Str
    :type job: Str
    """
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(3))
    password = fields.String(required=True, validate=validate.Length(8))
    job = fields.String(validate=validate.Length(2))

class NotebookModel(db.Model):
    """ Model for the notebook
    :type name: str
    :type id: int
    :type password: str
    :type user: UserModel
    """
    __tablename__ = 'notebooks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    port = db.Column(db.Integer, nullable=False)


    def __init__(self, name, password, user_id, port):
        self.name = name
        self.password = password
        self.user_id = user_id
        self.port = port 

class NotebookSchema(ma.Schema):
    """ Schema for the notebook
    :type id: Int
    :type name: Str
    :type password: Str
    :type user_id: Int
    """
    id = fields.Integer(dunp_only=True)
    name = fields.String(required=True, validate=validate.Length(3))
    password = fields.String(required=True, validate=validate.Length(8))
    user_id = fields.Integer(required=True)
    port = fields.Integer(required=True)
