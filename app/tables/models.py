from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.common.database import Base


class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(1000))
    datasets = relationship("Dataset", secondary="dataset_table_link")

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Table {self.name}>"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "datasets": [d.id for d in self.datasets],
        }


class DatasetTableLink(Base):
    __tablename__ = "dataset_table_link"
    dataset_id = Column(Integer, ForeignKey("datasets.id"), primary_key=True)
    table_id = Column(Integer, ForeignKey("tables.id"), primary_key=True)
