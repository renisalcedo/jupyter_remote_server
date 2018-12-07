from flask import request
from flask_restful import Resource
from ..Model import db, UserModel, UserSchema

users_schema = UserSchema(many=True)
user_schema = UserSchema()

class User(Resource):
    """ Get the user from the database """
    def get(self):
        users = UserModel.query.all()
        users = users_schema.dump(users).data

        return { "status": "Success", 'data': users }, 200

    def post(self):
        """ Creates user with the sent data
        :type username: str
        :type password: str
        :type job: str (optional)
        """
        json_data = request.get_json(force=True)
        not_valid = self.is_valid(json_data)

        # Only processes data when its valid
        if not not_valid:
            if not 'job' in json_data:
                job = None
            else:
                job = json_data['job']


            user = UserModel(
                username=json_data['username'],
                password=json_data['password']
            )

            db.session.add(user)
            db.session.commit()

            result = user_schema.dump(user).data

            return {"Status": "Success", 'data': result}, 200

        return not_valid


    def is_valid(self, json_data):
        """ Ensures the data can be added to the database
        :type json_data: json
        :rtype str
        """
        if not json_data:
            return {'Message': 'No data provided'}, 400

        # Data cannot be processed
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422

        # Finds the user in the database
        user = UserModel.query.filter_by(username=data['username']).first()

        if user:
            return {'Message': 'Username already exist'}, 400

        return False