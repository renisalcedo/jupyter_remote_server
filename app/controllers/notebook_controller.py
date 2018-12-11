from flask_restful import Resource
from flask import request
from IPython.lib import passwd
from ..Model import db, NotebookModel, NotebookSchema, UserModel

# Configuration classes
from .notebook_setting_controller import NotebookSetting
from .system_controller import SystemController

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

        # Creates the notebook with the given data
        self.create_notebook(notebook)

        db.session.add(notebook)
        db.session.commit()

        result = notebook_schema.dump(notebook).data
        return {"Status": "Success", 'data': result}, 200

    def create_notebook(self, notebook):
        """ Creates Notebook and sets system with given data
        :type json_data: Dic
        """
        port = 8888
        ip = '127.0.0.1'
        name = notebook.name
        # Initializes the notebook with given data
        name = 'genone' # TEMPORARY USER NAME TO TEST LOCALLY

        notebook_setting = NotebookSetting(notebook.password, port)
        notebook_system = SystemController(name, name, ip)

        # Creates and executes the notebook on the system
        notebook_data = notebook_setting.setting(name)
        notebook_system.init_files(notebook_data)