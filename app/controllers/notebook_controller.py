from flask_restful import Resource
from flask import request
from ..Model import db, NotebookModel, NotebookSchema

notebooks_schema = NotebookSchema(many=True)
notebooks_schemas = NotebookSchema()


class Notebook(Resource):
    def get(self):
        return {"Message": "Hello From Notebook"}

    def post(self):
        """ Creates user with the sent data
        :type name: str
        :type password: str
        :type user_id: int
        :rtype result: Json
        """
        json_data = request.get_json(force=True)

        # Only processes data when its valid
        notebook = NotebookModel(
            name=json_data['name'],
            password=json_data['password'],
            user_id = json_data['user_id']
        )

        db.session.add(notebook)
        db.session.commit()

        result = notebooks_schema.dump(notebook).data

        return {"Status": "Success", 'data': result}, 200