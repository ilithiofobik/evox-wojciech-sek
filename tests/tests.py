from fastapi import status
from fastapi.testclient import TestClient
from app import app
from app.schemas import MessageOnlyContent, MessageNoCounter

client = TestClient(app)


def test_unauthorised():
    response = client.post("/messages", json=MessageOnlyContent(Content="Lorem ipsum!").dict())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.put("/messages", json=MessageNoCounter(MessageID=1, Content="Lorem ipsum!").dict())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.delete("/messages/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login():
    response = client.get("/login?login=admin&password=evoxd")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.get("/login?login=admind&password=evox")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.get("/login?login=admin&password=evox")
    assert response.status_code == status.HTTP_202_ACCEPTED


def test_authorised():
    response = client.post("/messages", json=MessageOnlyContent(Content="Lorem ipsum lorem lorem.").dict())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    id = data['id']
    response = client.get(f"/messages/{id}")
    assert response.status_code == status.HTTP_200_OK
    response = client.get(f"/messages/{id + 1}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.put("/messages", json=MessageNoCounter(MessageID=id, Content="Lorem ipsum.").dict())
    assert response.status_code == status.HTTP_202_ACCEPTED
    response = client.put("/messages", json=MessageNoCounter(MessageID=id + 1, Content="Lorem ipsum.").dict())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete(f"/messages/{id + 1}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete(f"/messages/{id}")
    assert response.status_code == status.HTTP_202_ACCEPTED
    response = client.delete(f"/messages/{id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_logout():
    response = client.delete("/logout")
    assert response.status_code == status.HTTP_202_ACCEPTED
    response = client.delete("/logout")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_unauthorised2():
    response = client.post("/messages", json=MessageOnlyContent(Content="Lorem ipsum!").dict())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.put("/messages", json=MessageNoCounter(MessageID=1, Content="Lorem ipsum!").dict())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.delete("/messages/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
