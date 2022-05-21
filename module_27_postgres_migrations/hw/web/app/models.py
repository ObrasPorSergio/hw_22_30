from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, VARCHAR, ARRAY, Boolean, JSON
from sqlalchemy.orm import declarative_base, relationship
from typing import Dict, Any

Base = declarative_base()


class Coffee(Base):
    __tablename__ = 'coffees'

    id = Column(Integer, Sequence('coffee_id_seq'), primary_key=True, nullable=False)
    title = Column(VARCHAR(200), nullable=False)
    origin = Column(VARCHAR(200), nullable=True)
    intensifier = Column(VARCHAR(200), nullable=True)
    notes = Column(ARRAY(VARCHAR), nullable=True)

    def __repr__(self):
        return f"Coffee blend {self.title}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(VARCHAR(50), nullable=False)
    surname = Column(VARCHAR(50), nullable=True, default='Ivanov')
    patronimic = Column(VARCHAR(50), nullable=True)
    address = Column(JSON, nullable=True)
    coffee_id = Column(Integer, ForeignKey('coffees.id'))
    coffee = relationship("Coffee", backref="users")

    def __repr__(self):
        return f"User {self.name}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}
