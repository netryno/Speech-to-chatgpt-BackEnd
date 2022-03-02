from starlette.testclient import TestClient
from app.main import app
import json

client = TestClient(app)


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Fast API in Python'}


def test_read_poset():
    response = client.post('/my_post')
    assert response.status_code == 200
    assert response.json() == 1

