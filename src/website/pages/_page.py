"""Abstract class to dynamically render the right page with the right context"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar, Mapping, MutableMapping, Type

from flask import render_template

SERVER_DIR = Path(__file__).parent.parent
IMAGE_DIR = "static/img/topic"


class Page(ABC):
    """Abstract page"""

    _URL_MAPPING: ClassVar[MutableMapping[str, Type["Page"]]] = {}

    def __init_subclass__(cls, url: str) -> None:
        """Use dynamic registration of children to avoid circular dependencies"""
        super().__init_subclass__()
        if url in cls._URL_MAPPING.keys():
            raise Exception(
                f"{url} is already registered by {cls._URL_MAPPING[url].__name__} ({cls._URL_MAPPING[url].__module__})"
            )
        cls._URL_MAPPING[url] = cls

    @classmethod
    def render(cls, url: str, request_data: Mapping) -> str:
        """Render a single page from a template and a context object"""
        page = cls._URL_MAPPING[url]
        response = render_template(url, **(page.get_context(request_data)))
        return response

    @classmethod
    @abstractmethod
    def get_context(cls, request_data: Mapping) -> Mapping:
        """Return the dictionary with the data used to populate the template"""
