from flask_restful import Resource
from flask import request
from IPython.lib import passwd
from sqlalchemy.sql import func
from ..Model import db, NotebookModel, NotebookSchema, UserModel

# Configuration classes
from .notebook_setting_controller import NotebookSetting
from .system_controller import SystemController
import config

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
        not_valid = self.is_valid(json_data)

        if not not_valid:
            # Hashed password for jupyter notebook
            password = passwd(json_data['password'])

            # New Port number for new notebook
            port = self.get_new_port()
            url = "{0}:{1}".format(config.PUBLIC,port)

            # Only processes data when its valid
            notebook = NotebookModel(
                name=json_data['name'],
                password=password,
                user_id=json_data['user_id'],
                port=port,
                url=url
            )

            # Creates the notebook with the given data
            self.create_notebook(notebook)

            db.session.add(notebook)
            db.session.commit()

            result = notebook_schema.dump(notebook).data
            return {"Status": "Success", 'data': result}, 200

        return not_valid


    def create_notebook(self, notebook):
        """ Creates Notebook and sets system with given data
        :type json_data: Dic
        """
        # Initializes the notebook with given data
        notebook_setting = NotebookSetting(notebook.password, notebook.port)
        notebook_system = SystemController(notebook.name, notebook.name, notebook.port, config.IP)

        # Creates and executes the notebook on the system
        notebook_data = notebook_setting.setting(notebook.name, config.IP)
        notebook_system.init_files(notebook_data)

    def get_new_port(self):
        """ Returns a new port number everytime
        :rtype port: Int
        """
        max_port_number = db.session.query(func.max(NotebookModel.port).label('port_number')).one()
        max_port_number = max_port_number[0]

        if max_port_number:
            port = max_port_number + 1
        else:
            port = 8000

        return port

    def is_valid(self, json_data):
        """ Ensures the data can be added to the database
        :type json_data: json
        :rtype str
        """
        if not json_data:
            return {'Message': 'No data provided'}, 400

        # Data cannot be processed
        data, errors = notebook_schema.load(json_data)

        if errors and 'port' not in errors:
            return errors, 422

        # Finds the notebook in the database
        notebook = NotebookModel.query.filter_by(name=data['name']).first()

        if notebook:
            return {'Message': 'Notebook already exist'}, 400

        return False
