"""Context generator"""
from typing import Mapping

from website.pages._page import Page


class Index(Page, url="index.html"):
    """Context generator"""

    @classmethod
    def get_context(cls, request_data: Mapping) -> Mapping:
        """Return the dictionary with the data used to populate the template"""
        context = {"topic": request_data["topic"]}
        return context
