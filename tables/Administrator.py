from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref
from Db_Config import Base


class Administrator(Base):
    __tablename__ = 'administrators'

    id = Column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    user_id = Column(BigInteger(), ForeignKey('users.id'), nullable=False, unique=True, index=True)

    user = relationship("User", backref=backref("administrators", uselist=False))

    def __repr__(self):
        return f'\n<administrator id={self.id} first name={self.first_name} last name={self.last_name} ' \
               f'\nuser id={self.user_id}>'

    def __str__(self):
        return f'<administrator id={self.id} first name={self.first_name} last name={self.last_name} ' \
               f'\nuser id={self.user_id}>'
