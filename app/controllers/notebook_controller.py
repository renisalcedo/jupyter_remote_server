from flask_restful import Resource

class Notebook(Resource):
    def get(self):
        return {"Message": "Hello From Notebook"}