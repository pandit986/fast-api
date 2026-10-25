from fastapi.testclient import TestClient
from test_main import app


client = TestClient(app)

# Test the root endpoint
def test_read_root():
    response = client.get("/")
    # status_code check
    assert response.status_code == 200
    # json response check
    assert response.json() == {"message": "Hello, World!"}

# Test the add endpoint
def test_add_numbers():
    response = client.get("/add?a=5&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 8}