import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/jupyter_remote'
SECRET='The_Secret_Goes_Here'
IP="The_IP_Goes_Here"