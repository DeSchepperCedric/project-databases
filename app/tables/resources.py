from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import parser
from app.common.database import db_session
from app.tables.models import Table as TableModel


class TableList(Resource):
    """
    Represents a list of all tables
    """

    def get(self):
        """
        Returns the list of tables
        """
        return (
            {
                "message": "Success",
                "data": [t.serialize for t in TableModel.query.all()],
            },
            200,
        )

    def post(self):
        """
        Adds a new dataset
        """
        create_table_args = {
            "name": fields.Str(required=True),
            "description": fields.Str(),
        }
        args = parser.parse(create_table_args)
        table = TableModel(args["name"], args["description"])
        db_session.add(table)
        db_session.commit()
        return {"message": "Table added", "data": args}, 201


class Table(Resource):
    """
    Represents a single table, which contains rows
    """

    def get(self, table_id):
        """
        Returns a table
        """
        table = TableModel.query.filter_by(id=table_id).first()
        if table is None:
            return {"message": "Table not found"}, 200
        return {"message": "Success", "data": table.serialize}, 200

    def post(self, table_id):
        """
        Adds a new row to a table
        """
        return {"message": "Add row, not implemented", "data": {}}, 200

    def put(self, table_id):
        """
        Changes the name/description of a table
        """
        edit_table_args = {"name": fields.Str(), "description": fields.Str()}
        args = parser.parse(edit_table_args)

        table = TableModel.query.filter_by(id=table_id).first()

        table.name = args["name"]
        table.description = args["description"]

        db_session.commit()
        return {"message": "Table updated", "data": table.serialize}, 200

    def delete(self, table_id):
        """
        Deletes a table
        """
        table = TableModel.query.filter_by(id=table_id).first()
        db_session.delete(table)
        db_session.commit()
        return {"message": "Table deleted"}, 200
