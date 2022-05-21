from sqlalchemy import Column, String, Integer

from database import Base


class Recipie(Base):
    """Recipe model"""
    __tablename__ = 'Recipie'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    time = Column(Integer, index=True)
    count = Column(Integer)
    ingredients = Column(String, index=True)
    description = Column(String, index=True)
