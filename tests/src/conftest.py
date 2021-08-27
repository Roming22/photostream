from http import HTTPStatus
from typing import Callable, Generator, List

import pytest
from flask.testing import FlaskClient

from website.main import APP


@pytest.fixture
def client() -> Generator[  # pylint: disable=redefined-outer-name
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
