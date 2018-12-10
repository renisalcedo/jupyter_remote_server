from flask_restful import Resource
from flask import request
from IPython.lib import passwd
from ..Model import db, NotebookModel, NotebookSchema, UserModel

notebook_schemas = NotebookSchema(many=True)
notebook_schema = NotebookSchema()


class UserNotebook(Resource):
    def get(self):
        pass

    def post(self):
        """creates the users
        :type NotebookName: str
        :type user_id: Int

        :rtype result: Json
        """


        json_data = request.get_json(force=True)

        user_id = json_data['user_id']
        user = UserModel.query.filter_by(id=user_id).first()

        res = self.get_user_notebooks(user.notebooks)

        return {"status": "Success", 'data': res}, 200

    def get_user_notebooks(self, notebooks):
        """ this creates a loop so that it can print every notebook in the json

        :param notebooks:
        :return:
        """

        res = []

        for notebook in notebooks:
            data = {
                "name": notebook.name,
                "id": notebook.id
            }

            res.append(data)

        return res