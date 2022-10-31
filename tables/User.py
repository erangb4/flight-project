from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref
from Db_Config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger(), primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(), nullable=False, unique=True, index=True)
    password = Column(String(), nullable=False)
    email = Column(String(), nullable=False, unique=True, index=True)
    user_role = Column(Integer(), ForeignKey('user_roles.id'), nullable=False)

    role = relationship('UserRole', backref=backref("users", uselist=True))

    def __repr__(self):
        return f'\n<user id = {self.id}, username = {self.username}, password = {self.password}, email = {self.email},'\
               f'\n user role = {self.user_role}>'

    def __str__(self):
        return f'\n<user id = {self.id}, username = {self.username}, password = {self.password}, email = {self.email},'\
               f'\n user role = {self.user_role}>'
