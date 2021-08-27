"""Package registration"""
import website.pages.index
from website.pages._page import Page


def render(url: str):
    """Render a page based on the request URL"""
    return Page.render(url)
