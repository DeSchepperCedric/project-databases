from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import parser
from app.common.database import db_session
from app.datasets.models import Dataset as DatasetModel
from app.tables.models import Table as TableModel


class DatasetList(Resource):
    """
    Represents a list of all datasets
    """

    def get(self):
        """
        Returns the list of datasets
        """
        return (
            {
                "message": "Success",
                "data": [d.serialize for d in DatasetModel.query.all()],
            },
            200,
        )

    def post(self):
        """
        Adds a new dataset
        """
        create_dataset_args = {
            "name": fields.Str(required=True),
            "description": fields.Str(),
            "tables": fields.DelimitedList(fields.Int, delimiter=","),
        }
        args = parser.parse(create_dataset_args)
        dataset = DatasetModel(args["name"], args["description"])
        tables = TableModel.query.filter(TableModel.id.in_(args["tables"])).all()
        for table in tables:
            dataset.tables.append(table)
        db_session.add(dataset)
        db_session.commit()
        return {"message": "Dataset added", "data": args}, 201


class Dataset(Resource):
    """
    Represents a single dataset, which contains tables
    """

    def get(self, dataset_id):
        """
        Returns a dataset
        """
        dataset = DatasetModel.query.filter_by(id=dataset_id).first()
        if dataset is None:
            return {"message": "Dataset not found"}, 200
        return {"message": "Success", "data": dataset.serialize}, 200

    def post(self, dataset_id):
        """
        Adds a new table to a dataset
        """
        add_table_args = {"name": fields.Str(), "description": fields.Str()}
        args = parser.parse(add_table_args)

        table = TableModel(args["name"], args["description"])
        table_id = table.id

        db_session.add(table)
        db_session.commit()

        return {"message": "Table added", "data": table.serialize}, 200

    def put(self, dataset_id):
        """
        Changes the name/description of a dataset
        """
        edit_dataset_args = {"name": fields.Str(), "description": fields.Str()}
        args = parser.parse(edit_dataset_args)

        dataset = DatasetModel.query.filter_by(id=dataset_id).first()

        dataset.name = args["name"]
        dataset.description = args["description"]

        db_session.commit()
        return {"message": "Dataset updated", "data": dataset.serialize}, 200

    def delete(self, dataset_id):
        """
        Deletes a dataset
        """
        dataset = DatasetModel.query.filter_by(id=dataset_id).first()
        db_session.delete(dataset)
        db_session.commit()
        return {"message": "Dataset deleted"}, 200
