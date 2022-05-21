import json
from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///parking_net.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, Parking, ClientParking

    @app.before_first_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients", methods=['GET'])
    def get_client_handler():
        """Get all clients"""
        clients: List[Client] = db.session.query(Client).all()
        clients_listed = [client.to_json() for client in clients]
        return jsonify(clients_listed), 200

    @app.route("/clients/<int:client_id>", methods=['GET'])
    def get_user_handler(client_id: int):
        """Get client by id"""
        client: Client = db.session.query(Client).get(client_id)
        return jsonify(client.to_json()), 200

    @app.route("/clients", methods=['POST'])
    def create_client_handler():
        """Create new client"""
        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        credit_card = request.form.get('credit_card', type=str)
        car_number = request.form.get('car_number', type=str)

        new_client = Client(name=name,
                            surname=surname,
                            credit_card=credit_card,
                            car_number=car_number)

        db.session.add(new_client)
        db.session.commit()

        return jsonify(new_client.to_json()), 201

    @app.route("/parkings", methods=['POST'])
    def create_parking_lot_handler() :
        """Create new parking lot"""
        address = request.form.get('address', type=str)
        count_places = request.form.get('count_places', type=str)

        new_parking = Parking(address=address,
                              count_places=count_places,
                              count_available_places=count_places)

        db.session.add(new_parking)
        db.session.commit()

        return jsonify(new_parking.to_json()), 201

    @app.route("/client_parkings", methods=['POST'])
    def create_parking_enter():
        """Create enter in parking"""
        client_id = request.form.get('client_id', type=int)
        parking_id = request.form.get('parking_id', type=int)
        parking = db.session.query(Parking).get(parking_id)
        if parking and parking.count_available_places > 0 and parking.opened:
            new_enter_parking = ClientParking(client_id=client_id,
                                              parking_id=parking_id)
            parking.count_available_places -= 1
            db.session.add(new_enter_parking)
            db.session.commit()

            return jsonify(new_enter_parking.to_json()), 201
        return json.dumps({'response': 'No free places or closed'}), 409

    @app.route("/client_parkings", methods=['DELETE'])
    def create_parking_leave() :
        """Create leaving the parking"""
        client_id = request.form.get('client_id', type=int)
        parking_id = request.form.get('parking_id', type=int)
        client = db.session.query(Client).get(client_id)
        parking = db.session.query(Parking).get(parking_id)
        client_parking = db.session.query(ClientParking).filter_by(
            client_id=client_id,
            parking_id=parking_id,
            time_out=None
            ).first()

        if parking and client and client_parking:
            if client.credit_card:
                parking.count_available_places += 1
                client_parking.time_out = datetime.utcnow()
                db.session.commit()
                return jsonify(client_parking.to_json()), 201
            return json.dumps({'response': 'You can not leave without having paid'}), 409
        return json.dumps({'response': 'No such client, parking or client has already left'}), 409

    return app
