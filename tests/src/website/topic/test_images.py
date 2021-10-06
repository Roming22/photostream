from typing import Callable

TOPIC = "unittest"
URL = f"/{TOPIC}/images"


def test_endpoint_methods(assert_endpoint_methods: Callable) -> None:
    assert_endpoint_methods(URL, ["GET", "HEAD", "OPTIONS"])


def test_page(page_tester: Callable) -> None:
    data = page_tester(URL)
    assert sorted(data["images"], key=lambda item: item["filename"]) == [
        {"filename": "photo1.jpg", "url": "/static/img/topic/unittest/photo1.jpg"},
        {"filename": "photo2.jpg", "url": "/static/img/topic/unittest/photo2.jpg"},
        {"filename": "photo3.jpg", "url": "/static/img/topic/unittest/photo3.jpg"},
        {"filename": "photo4.jpg", "url": "/static/img/topic/unittest/photo4.jpg"},
    ]
