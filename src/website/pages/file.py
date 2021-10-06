"""Context generator"""
from json import dumps
from typing import Mapping

from website.pages._page import IMAGE_DIR, SERVER_DIR, Page


class File(Page, url="file.json"):
    """Context generator"""

    @classmethod
    def get_context(cls, request_data: Mapping) -> Mapping:
        """Return the dictionary with the data used to populate the template"""
        if request_data["http_method"] == "DELETE":
            data = cls.delete_file(request_data["topic"], request_data["filename"])
        context = {"data": dumps(data)}
        return context

    @classmethod
    def delete_file(cls, topic: str, filename: str) -> Mapping:
        """Delete a file

        :param filename: file to delete.
        :param topic: topic in which the file is located.

        :return: A map with the file attributes.
        """
        filepath = SERVER_DIR / IMAGE_DIR / topic / filename
        filepath.unlink()
        data = {
            "filepath": f"{filepath}",
            "delete": True,
        }
        return data
