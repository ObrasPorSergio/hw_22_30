import pytest
from parking.main.app import create_app, db as _db
from parking.main.models import Client, Parking, ClientParking


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "parking_test: 'parking_test'"
    )

@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()

        for index in range(1, 4):
            if index < 3:
                credit_card = f"{index}111222233334444"
            else:
                credit_card = ""
            client = Client(name=f"test_name_{index}",
                            surname=f"test_surname_{index}",
                            credit_card=credit_card,
                            car_number=f"e{index}56se")
            _db.session.add(client)

        parking = Parking(address="test address",
                          count_places=5,
                          count_available_places=5)

        client_parking = ClientParking(client_id=1,
                                       parking_id=1)

        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
