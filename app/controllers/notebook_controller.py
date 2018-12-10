from flask_restful import Resource
from flask import request
from IPython.lib import passwd
from ..Model import db, NotebookModel, NotebookSchema, UserModel

notebook_schemas = NotebookSchema(many=True)
notebook_schema = NotebookSchema()

class Notebook(Resource):
    def get(self):
        notebooks = NotebookModel.query.all()
        notebooks = notebook_schemas.dump(notebooks).data

        return { "status": "Success", 'data': notebooks }, 200

    def post(self):
        """ Creates user with the sent data
        :type name: str
        :type password: str
        :type user_id: int
        :rtype result: Json
        """
        json_data = request.get_json(force=True)

        # Hashed password for jupyter notebook
        password = passwd(json_data['password'])

        # Only processes data when its valid
        notebook = NotebookModel(
            name=json_data['name'],
            password=password,
            user_id = json_data['user_id']
        )

        db.session.add(notebook)
        db.session.commit()

        result = notebook_schema.dump(notebook).data

        return {"Status": "Success", 'data': result}, 200