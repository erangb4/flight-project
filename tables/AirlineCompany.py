from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, backref
from Db_Config import Base


class AirlineCompany(Base):
    __tablename__ = 'airline_companies'

    id = Column(BigInteger(), primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(), nullable=False, unique=True, index=True)
    country_id = Column(BigInteger(), ForeignKey('countries.id'), nullable=False)
    user_id = Column(BigInteger(), ForeignKey('users.id'), nullable=False, unique=True, index=True)

    user = relationship('User', backref=backref("airline_companies", uselist=False))

    def __repr__(self):
        return f'\n<Airline Company id={self.id} name={self.name} country id={self.country_id} user id={self.user_id}>'

    def __str__(self):
        return f'<Airline Company id={self.id} name={self.name} country id={self.country_id} user id={self.user_id}>'
