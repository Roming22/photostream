from http import HTTPStatus

from flask.testing import FlaskClient


def test_404(client: FlaskClient) -> None:
    response = client.get("/does_not_exists")
    assert response.status_code == HTTPStatus.NOT_FOUND
