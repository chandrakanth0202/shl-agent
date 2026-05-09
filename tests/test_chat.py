from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health():

    response = client.get("/health")

    assert response.status_code == 200

def test_chat():

    response = client.post(
        "/chat",
        json={
            "messages": [
                {
                    "role": "user",
                    "content": "Need senior Python assessment"
                }
            ]
        }
    )

    assert response.status_code == 200