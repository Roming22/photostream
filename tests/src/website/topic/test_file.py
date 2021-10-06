import pathlib
from http import HTTPStatus
from json import loads
from typing import Callable
from unittest.mock import Mock

from flask.testing import FlaskClient
from pytest import MonkeyPatch

from website.pages._page import IMAGE_DIR, SERVER_DIR

TOPIC = "unittest"
URL = f"/{TOPIC}/file"
FILE = "photo1.jpg"


def test_endpoint_methods(assert_endpoint_methods: Callable) -> None:
    assert_endpoint_methods(f"{URL}/{FILE}", ["DELETE", "OPTIONS"])


def test_get_filename(monkeypatch: MonkeyPatch, client: FlaskClient) -> None:
    mock_unlink = Mock()
    monkeypatch.setattr(pathlib.Path, "unlink", mock_unlink)
    response = client.delete(f"{URL}/{FILE}")
    assert response.status_code == HTTPStatus.OK
    assert mock_unlink.call_count == 1
    data = loads(response.data)
    assert data == {
        "filepath": (SERVER_DIR / IMAGE_DIR / TOPIC / FILE).as_posix(),
        "delete": True,
    }
