from flask import Flask
from flask_restful import Resource, Api

from api.library_api import *
from db.swen344_db_utils import exec_sql_file

app = Flask(__name__)
api = Api(app)

api.add_resource(user, '/user')
api.add_resource(inventory, '/books')
api.add_resource(inventoryGenreTitle, '/books/<string:attribute>/<string:text>')
api.add_resource(userLogin, '/userLogin')
api.add_resource(userDelete, '/user/<string:username>/<string:session_key>')
api.add_resource(userUpdate, '/userUpdate')
api.add_resource(checkOutBook, '/checkOutBook')
api.add_resource(checkOutBookID, '/checkOutBook/<string:username>')

if __name__ == '__main__':
    exec_sql_file('src/db/set_up.sql')
    exec_sql_file('tests/db/test_db.sql')
    app.run(debug=True, port=4999),
