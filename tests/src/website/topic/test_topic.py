from http import HTTPStatus
from typing import Callable
from unittest.mock import Mock

from flask.testing import FlaskClient
from pytest import MonkeyPatch

import website.pages.index

TOPIC = "unittest"
URL = f"/{TOPIC}"


def test_endpoint_methods(assert_endpoint_methods: Callable) -> None:
    assert_endpoint_methods(URL, ["GET", "HEAD", "OPTIONS"])


def test_page(monkeypatch: MonkeyPatch, client: FlaskClient) -> None:
    mock_choice = Mock(return_value=f"static/img/{TOPIC}/photo1.jpg")
    monkeypatch.setattr(website.pages.index, "choice", mock_choice)
    response = client.get(URL)
    assert response.status_code == HTTPStatus.OK
    assert mock_choice.call_count == 1
    call_args = {str(arg) for arg in mock_choice.call_args_list[0].args[0]}
    assert call_args == {
        "static/img/unittest/photo1.jpg",
        "static/img/unittest/photo2.jpg",
        "static/img/unittest/photo3.jpg",
        "static/img/unittest/photo4.jpg",
    }