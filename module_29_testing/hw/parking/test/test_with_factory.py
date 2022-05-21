from .factories import ClientFactory, ParkingFactory
from parking.main.models import Client, Parking


def test_create_client(app, db):
    client = ClientFactory()
    db.session.commit()
    assert client.id == 4
    assert len(db.session.query(Client).all()) == 4


def test_create_product(app, db):
    parking = ParkingFactory()
    db.session.commit()
    assert parking.id == 2
    assert len(db.session.query(Parking).all()) == 2
