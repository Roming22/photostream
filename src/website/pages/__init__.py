"""Package registration"""
from typing import Mapping

import website.pages.file
import website.pages.images
import website.pages.index
import website.pages.topic
from website.pages._page import Page


def render(url: str, request_data: Mapping) -> str:
    """Render a page based on the request URL"""
    return Page.render(url, request_data)
