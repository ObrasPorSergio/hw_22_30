import pytest
from parking.main.models import Client, Parking, ClientParking


@pytest.mark.parametrize("route", ["/clients", "/clients/1"])
def test_route_status(client, route):
    response = client.get(route)
    assert response.status_code == 200


def test_create_client(client) -> None:
    client_data = {"name": "Jon", "surname": "Doe",
                   "credit_card": "11114444", "car_number": "o567rt"}
    response = client.post("/clients", data=client_data)

    assert b"Doe" in response.data
    assert response.status_code == 201


def test_create_parking(client) -> None:
    parking_data = {"address": "Via Nova 1", "count_places": 10}
    response = client.post("/parkings", data=parking_data)

    assert b"count_available_places" in response.data
    assert b"Nova" in response.data
    assert response.status_code == 201


@pytest.mark.parking_test
def test_enter_open_parking(client, db) -> None:
    parking_data = {"client_id": 2, "parking_id": 1}
    parking = db.session.query(Parking).first()
    free_places = parking.count_available_places
    response = client.post("/client_parkings", data=parking_data)
    parking = db.session.query(Parking).first()
    left_spaces = parking.count_available_places
    assert free_places > left_spaces
    assert b"client_id" in response.data
    assert response.status_code == 201


@pytest.mark.parking_test
def test_enter_closed_parking(client, db) -> None:
    parking_data = {"client_id": 2, "parking_id": 1}
    parking = db.session.query(Parking).first()
    parking.opened = False
    response = client.post("/client_parkings", data=parking_data)
    assert b"No free places or closed" in response.data
    assert response.status_code == 409


@pytest.mark.parking_test
def test_enter_full_parking(client, db) -> None:
    parking_data = {"client_id": 2, "parking_id": 1}
    parking = db.session.query(Parking).first()
    parking.count_available_places = 0
    response = client.post("/client_parkings", data=parking_data)
    assert b"No free places or closed" in response.data
    assert response.status_code == 409


@pytest.mark.parking_test
def test_enter_parking_successfully(client, db) -> None:
    parking_data = {"client_id": 1, "parking_id": 1}
    parking = db.session.query(Parking).first()
    available_before = parking.count_available_places
    response = client.delete("/client_parkings", data=parking_data)
    client_parking = db.session.query(ClientParking).first()
    parking = db.session.query(Parking).first()
    available_after = parking.count_available_places
    enter_time = client_parking.time_in
    exit_time = client_parking.time_out
    assert exit_time > enter_time
    assert available_after > available_before
    assert b"client_id" in response.data
    assert response.status_code == 201

    response = client.delete("/client_parkings", data=parking_data)
    assert b"already left" in response.data
    assert response.status_code == 409


@pytest.mark.parking_test
def test_enter_parking_unsuccessfully(client, db) -> None:
    parking_data = {"client_id": 3, "parking_id": 1}
    client.post("/client_parkings", data=parking_data)
    response = client.delete("/client_parkings", data=parking_data)
    assert b"without having paid" in response.data
    assert response.status_code == 409
