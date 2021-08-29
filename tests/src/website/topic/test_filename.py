from http import HTTPStatus
from pathlib import Path
from typing import Callable
from unittest.mock import Mock

from flask.testing import FlaskClient
from pytest import MonkeyPatch

import website.pages.filename
from website.pages.filename import IMAGE_DIR, SERVER_DIR

TOPIC = "unittest"
URL = f"/{TOPIC}"
FILE = "photo1.jpg"


def test_endpoint_methods(assert_endpoint_methods: Callable) -> None:
    assert_endpoint_methods(URL, ["GET", "HEAD", "OPTIONS"])


def assert_photo(response) -> None:
    assert response.status_code == HTTPStatus.OK


def test_get_random(monkeypatch: MonkeyPatch, client: FlaskClient) -> None:
    mock_choice = Mock(return_value=Path(f"{SERVER_DIR}/{IMAGE_DIR}/{TOPIC}/{FILE}"))
    monkeypatch.setattr(website.pages.filename, "choice", mock_choice)
    response = client.get(f"{URL}/random")
    assert_photo(response)
    assert mock_choice.call_count == 1
    call_args = {str(arg) for arg in mock_choice.call_args_list[0].args[0]}
    assert call_args == {
        f"{SERVER_DIR}/{IMAGE_DIR}/{TOPIC}/{FILE}",
        f"{SERVER_DIR}/{IMAGE_DIR}/{TOPIC}/photo2.jpg",
        f"{SERVER_DIR}/{IMAGE_DIR}/{TOPIC}/photo3.jpg",
        f"{SERVER_DIR}/{IMAGE_DIR}/{TOPIC}/photo4.jpg",
    }


def test_get_filename(monkeypatch: MonkeyPatch, client: FlaskClient) -> None:
    mock_unlink = Mock()
    mock_path = Mock(unlink=mock_unlink)
    monkeypatch.setattr(website.pages.filename, "Path", mock_path)
    response = client.get(f"{URL}/{FILE}")
    assert_photo(response)
    # assert mock_unlink.call_count == 1
