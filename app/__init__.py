from flask import Blueprint
from flask_restful import Api
from .controllers.notebook_controller import Notebook
from .controllers.user_controller import User
from .controllers.user_notebook_controller import UserNotebook
from .auth.auth import Auth

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Notebook, '/notebook')
api.add_resource(User, '/user')
api.add_resource(UserNotebook, '/user/notebook')
api.add_resource(Auth, '/auth')