from typing import Callable

TOPIC = "unittest"
URL = f"/{TOPIC}"


def test_endpoint_methods(assert_endpoint_methods: Callable) -> None:
    assert_endpoint_methods(URL, ["GET", "HEAD", "OPTIONS"])


def test_page(page_tester: Callable) -> None:
    page_tester(URL)
