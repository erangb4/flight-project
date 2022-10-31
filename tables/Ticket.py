from sqlalchemy import Column, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from Db_Config import Base


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(BigInteger(), primary_key=True, nullable=False, autoincrement=True)
    flight_id = Column(BigInteger(), ForeignKey('flights.id'), nullable=False)
    customer_id = Column(BigInteger(), ForeignKey('customers.id'), nullable=False)

    __table_args__ = (UniqueConstraint('flight_id', 'customer_id', name='una_1'),)

    flight = relationship("Flight", backref=backref("tickets", uselist=True))
    customer = relationship("Customer", backref=backref("tickets", uselist=True))

    def __repr__(self):
        return f'\n<Ticket id = {self.id}, flight id = {self.flight_id}, customer id = {self.customer_id}>'

    def __str__(self):
        return f'\n<Ticket id = {self.id}, flight id = {self.flight_id}, customer id = {self.customer_id}>'
