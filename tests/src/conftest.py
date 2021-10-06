from http import HTTPStatus
from json import loads
from json.decoder import JSONDecodeError
from typing import Callable, Generator, List, Mapping

import pytest
from flask.testing import FlaskClient

from website.routing import APP


@pytest.fixture(name="client")
def fixture_client() -> Generator[  # pylint: disable=redefined-outer-name
    FlaskClient, None, None
]:
    with APP.test_client() as test_client:
        yield test_client


@pytest.fixture
def assert_endpoint_methods(
    client: FlaskClient,  # pylint: disable=redefined-outer-name
) -> Callable:
    def _test(url: str, methods: List[str]) -> None:
        response = client.options(url)
        assert response.status_code == HTTPStatus.OK
        assert sorted(response.headers["Allow"].split(", ")) == sorted(methods)

    return _test


@pytest.fixture
def page_tester(client: FlaskClient) -> Callable:
    def _func(url: str) -> Mapping:
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        data = response.data
        try:
            data = loads(response.data)
        except JSONDecodeError:
            pass
        return data

    return _func
