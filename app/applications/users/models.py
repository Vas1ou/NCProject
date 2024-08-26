from sqlalchemy.orm import relationship
from db.base import Base
from sqlalchemy import Column, Integer, String
from applications.orders.models import Order


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    orders = relationship(Order, back_populates='user')
