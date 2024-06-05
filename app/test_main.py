from .cloudesire_client import settings
from .main import app
from fastapi.testclient import TestClient
from httpx import Response
import pytest


client = TestClient(app)


@pytest.mark.respx(base_url=settings.cmw_base_url)
def test_created_event(respx_mock):
    respx_mock.get("/subscription/1").mock(
        return_value=Response(
            200, json={"id": 1, "deploymentStatus": "PENDING", "paid": True}
        )
    )
    response = client.post(
        "/event", json={"entity": "Subscription", "id": 1, "type": "CREATED"}
    )
    assert response.status_code == 204
