from http import HTTPStatus
from typing import Callable

from flask.testing import FlaskClient

TOPIC = "unittest"
URL = f"/{TOPIC}"


def test_endpoint_methods(assert_endpoint_methods: Callable) -> None:
    assert_endpoint_methods(URL, ["GET", "HEAD", "OPTIONS"])


def test_page(client: FlaskClient) -> None:
    response = client.get(URL)
    assert response.status_code == HTTPStatus.OK
