from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref
from Db_Config import Base


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(BigInteger(), primary_key=True, nullable=False, autoincrement=True)
    airline_company_id = Column(BigInteger(), ForeignKey('airline_companies.id'), nullable=False)
    origin_country_id = Column(Integer(), ForeignKey('countries.id'), nullable=False)
    destination_country_id = Column(Integer(), ForeignKey('countries.id'), nullable=False)
    departure_time = Column(DateTime(), default=datetime.utcnow())
    landing_time = Column(DateTime(), default=datetime.utcnow())
    remaining_tickets = Column(Integer(), nullable=False)

    airline_company = relationship('AirlineCompany', backref=backref("flights", uselist=True))
    origin_county = relationship('Country', foreign_keys=[origin_country_id],
                                 backref=backref("oc_flights", uselist=True))
    destination_county = relationship('Country', foreign_keys=[destination_country_id],
                                      backref=backref("dc_flights", uselist=True))

    def __repr__(self):
        return f'\n<flight id={self.id} airline company id={self.airline_company_id}' + \
               f'\n origin country id={self.origin_country_id} destination country id={self.destination_country_id}' + \
               f'\n departure time={self.departure_time} landing time={self.landing_time}' + \
               f'\n remaining tickets={self.remaining_tickets}>'

    def __str__(self):
        return f'<flight id={self.id} airline company id={self.airline_company_id}' + \
               f'\n origin country id={self.origin_country_id} destination country id={self.destination_country_id}' + \
               f'\n departure time={self.departure_time} landing time={self.landing_time}' + \
               f'\n remaining tickets={self.remaining_tickets}>'
