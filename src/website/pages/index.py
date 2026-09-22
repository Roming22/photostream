"""Context generator"""

from typing import Mapping

from website.pages._page import IMAGE_DIR, SERVER_DIR, Page


class Index(Page, url="index.html"):
    """Context generator"""

    @classmethod
    def get_context(cls, request_data: Mapping) -> Mapping:
        """Return the dictionary with the data used to populate the template"""
        topic_dir = SERVER_DIR / IMAGE_DIR
        topics = sorted(
            d.name
            for d in topic_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )
        return {"topics": topics}
