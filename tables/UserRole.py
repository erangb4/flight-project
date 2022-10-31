from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from Db_Config import Base


class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    role_name = Column(String(), nullable=False, unique=True, index=True)

    def __repr__(self):
        return f'\n<user role id={self.id} role name={self.role_name}>'

    def __str__(self):
        return f'<user role id={self.id} role name={self.role_name}>'
