from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref
from Db_Config import Base


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(BigInteger(), primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    address = Column(String(), nullable=False)
    phone_no = Column(String(), nullable=False, unique=True, index=True)
    credit_card_no = Column(String(), nullable=False, unique=True, index=True)
    user_id = Column(BigInteger(), ForeignKey('users.id'), nullable=False, unique=True, index=True)

    user = relationship("User", backref=backref("customers", uselist=False))

    def __repr__(self):
        return f'\n<customer id={self.id} first name={self.first_name} last name={self.last_name}' + \
               f'\n address={self.address} phone number={self.phone_no} credit card number={self.credit_card_no}' + \
               f'\n user id={self.user_id}>'

    def __str__(self):
        return f'<customer id={self.id} first name={self.first_name} last name={self.last_name}' + \
               f'\n address={self.address} phone number={self.phone_no} credit card number={self.credit_card_no}' + \
               f'\n user id={self.user_id}>'
