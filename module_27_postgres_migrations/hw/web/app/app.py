import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify, request, json
from models import Coffee, User, Base
from info_requester import get_data

URL_COFFEE = 'https://random-data-api.com/api/coffee/random_coffee'
URL_USER = 'https://random-data-api.com/api/users/random_user'
URL_ADDRESS = 'https://random-data-api.com/api/address/random_address'

app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://admin:admin@postgres/skillbox_db')
# engine = create_engine('postgresql+psycopg2://admin:admin@0.0.0.0:5432')
Session = sessionmaker(bind=engine)
session = Session()


@app.before_first_request
def before_request_func() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    coffee_data = get_data(URL_COFFEE, 10)

    objects = []
    for index in range(10):
        data = coffee_data[index]
        notes = data['notes'].split(', ')
        coffee = Coffee(title=data['blend_name'], origin=data['origin'],
                        notes=notes, intensifier=data['intensifier'])
        objects.append(coffee)

    session.bulk_save_objects(objects)
    session.commit()

    people = get_data(URL_USER, 10)
    addresses = get_data(URL_ADDRESS, 10)

    objects = []
    for index in range(10):
        person = random.choice(people)
        user = User(name=person['first_name'], address=addresses[index], coffee_id=random.randint(1, 10))
        objects.append(user)

    session.bulk_save_objects(objects)
    session.commit()


@app.route('/users', methods=['POST'])
def new_user() -> json:
    name = request.form.get('name', type=str)
    addresses = get_data(URL_ADDRESS, 1)

    user = User(name=name, address=addresses[0], coffee_id=random.randint(1, 10))
    session.add(user)
    session.commit()

    coffee = session.query(Coffee).filter(Coffee.id == user.coffee_id).first()

    user_obj = user.to_json()
    del user_obj['coffee_id']
    user_obj['coffee'] = coffee.title

    return jsonify(user_obj)


@app.route('/users', methods=['GET'])
def get_users() -> json:
    country = request.args.get('country')
    users = session.query(User).all()
    elements = []

    for user in users:
        if country:
            user_country = user.address['country']
            if country == user_country:
                user_obj = user.to_json()
                elements.append(user_obj)
        else:
            user_obj = user.to_json()
            elements.append(user_obj)
    return jsonify(elements)


@app.route('/coffee', methods=['GET'])
def get_coffee() -> json:
    sort = request.args.get('sort')
    if sort:
        coffees = session.query(Coffee).filter(Coffee.title.match(sort)).all()
    else:
        coffees = session.query(Coffee).all()

    elements = []
    for coffee in coffees:
        coffee_obj = coffee.to_json()
        elements.append(coffee_obj)
    return jsonify(elements)


@app.route('/notes', methods=['GET'])
def get_notes() -> json:
    coffees = session.query(Coffee).all()

    elements = []
    for coffee in coffees:
        for elem in coffee.notes:

            if elem in elements:
                elements.remove(elem)
            else:
                elements.append(elem)

    return {'unique notes': elements}


if __name__ == '__main__':
    app.run()
