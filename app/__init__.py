from flask import Flask, Blueprint
from flask_restful import Api
from app.datasets.resources import DatasetList, Dataset
from app.tables.resources import TableList, Table
from app.common.database import db_session

app = Flask(__name__)
api_bp = Blueprint("api", __name__)
api = Api(app, prefix="/api")

api.add_resource(DatasetList, "/datasets")
api.add_resource(Dataset, "/datasets/<dataset_id>")
api.add_resource(TableList, "/tables")
api.add_resource(Table, "/tables/<table_id>")

app.register_blueprint(api_bp)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove
