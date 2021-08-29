"""Package registration"""
from typing import Mapping

import website.pages.filename
import website.pages.index
from website.pages._page import Page


def render(url: str, request_data: Mapping) -> str:
    """Render a page based on the request URL"""
    return Page.render(url, request_data)
