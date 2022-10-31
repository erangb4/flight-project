from sqlalchemy import Column, Integer, String
from Db_Config import Base


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(), nullable=False, unique=True, index=True)

    def __repr__(self):
        return f'\n<Country id={self.id} name={self.name}>'

    def __str__(self):
        return f'<Country id={self.id} name={self.name}>'
