from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_list_page():
    response = client.get('/')
    assert response.status_code == 200
    assert b'List' in response.content
    assert b'Detail' not in response.content


def test_detail_page():
    response = client.get('/1')
    assert response.status_code == 200
    assert b'detail' in response.content
    assert b'List' not in response.content


def test_add_method():
    response = client.post('/add/', json={
        "title": "new dish",
        "time": 45,
        "count": 0,
        "ingredients": "test ingredients",
        "description": "test description"
    })
    assert response.status_code == 200
    assert response.json()['title'] == "new dish"
    assert response.json()['description'] == "test description"
