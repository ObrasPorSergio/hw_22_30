import factory
import factory.fuzzy as fuzzy
import random

from parking.main.app import create_app, db
from parking.main.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = fuzzy.FuzzyChoice(['', '11112222'])
    car_number = fuzzy.FuzzyText(prefix='t', chars=[str(x) for x in range(9)], suffix='ks', length=6)


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('address')
    opened = fuzzy.FuzzyChoice([False, True])
    count_places = fuzzy.FuzzyInteger(low=100, high=150)
    count_available_places = factory.LazyAttribute(lambda x: random.randrange(0, 100))
