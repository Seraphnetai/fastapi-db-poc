from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_healthcheck():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'Server available'
