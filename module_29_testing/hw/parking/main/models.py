from .app import db
from typing import Dict, Any
from datetime import datetime


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50), nullable=True)
    car_number = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f"Клиент {self.name} {self.surname}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class Parking(db.Model):
    __tablename__ = 'parkings'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean, default=True)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Парковка по адресу {self.address}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class ClientParking(db.Model):
    __tablename__ = 'client_parkings'
    __table_args__ = (db.UniqueConstraint('client_id', 'parking_id', name="unique_client_parking"),)

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    parking_id = db.Column(db.Integer, db.ForeignKey('parkings.id'))
    time_in = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    time_out = db.Column(db.DateTime, nullable=True)

    client = db.relationship("Client", backref="client_parkings")
    parking = db.relationship("Parking", backref="client_parkings")

    def __repr__(self):
        return f"Парковка {self.client.name} по адресу {self.parking.address}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}