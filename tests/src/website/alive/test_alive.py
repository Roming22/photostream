from typing import Callable


def test_endpoint_methods(assert_endpoint_methods: Callable) -> None:
    assert_endpoint_methods("/alive", ["GET", "HEAD", "OPTIONS"])
