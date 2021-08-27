import datetime
from http import HTTPStatus
from typing import Callable
from unittest.mock import Mock

from flask.testing import FlaskClient
from pytest import MonkeyPatch

import website.pages.index


def test_endpoint_methods(assert_endpoint_methods: Callable) -> None:
    assert_endpoint_methods("/", ["GET", "HEAD", "OPTIONS"])


def test_page(monkeypatch: MonkeyPatch, client: FlaskClient) -> None:
    mock_datetime = Mock(spec=datetime.datetime)
    mock_datetime.now = Mock(return_value=datetime.datetime(2020, 1, 31, 12, 30, 42))
    monkeypatch.setattr(website.pages.index, "datetime", mock_datetime)
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert mock_datetime.now.call_count == 1
