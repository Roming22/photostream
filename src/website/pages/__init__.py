"""Package registration"""
from typing import Mapping, MutableMapping

import website.pages.filename
import website.pages.index
import website.pages.topic
from website.pages._page import Page


def render(url: str, request_data: Mapping, context: MutableMapping) -> str:
    """Render a page based on the request URL"""
    return Page.render(url, request_data, context)
