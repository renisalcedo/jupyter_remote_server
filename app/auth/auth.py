import jwt
import bcrypt
from flask import request
from flask_restful import Resource
from ..Model import db, UserModel, UserSchema
import config

user_schema = UserSchema()

class Auth(Resource):
    def post(self):
        """ Sign User in
        :type username: Str
        :type password: Str
        :rtype result: Dic(Str)
        """
        json_data = request.get_json(force=True)
        data, errors = user_schema.load(json_data)

        if errors:
            return errors, 422

        # Finds the user in the database
        user = UserModel.query.filter_by(username=data['username']).first()

        # User does not exist in database
        if not user:
            return {'Message': 'That username does not exist'}, 400

        # Check password
        password = json_data['password']
        user_password = str(user.password)
        correct_password = bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8'))

        # Return data when password is correct
        if correct_password:
            result = user_schema.dump(user).data

            jwt_token =  str(jwt.encode(result, config.SECRET, algorithm='HS256'))

            # Return Response data and token
            return { "Status": "Success", "data": result, "token": jwt_token }, 200

        return { "Message": "Incorrect Password" }, 400