"""Context generator"""
from datetime import datetime
from typing import Mapping

from website.pages._page import Page


class Index(Page, url="index.html"):
    """Context generator"""

    @classmethod
    def get_context(cls) -> Mapping:
        """Return the dictionary with the data used to populate the template"""
        context = {"time": cls.get_time()}
        return context

    @staticmethod
    def get_time() -> str:
        """Get the current time"""
        time = datetime.now().strftime("%H:%M:%S")
        return time
