from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.common.database import Base


class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(1000))
    tables = relationship("Table", secondary="dataset_table_link")

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Dataset {self.name}>"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tables": [t.id for t in self.tables],
        }
