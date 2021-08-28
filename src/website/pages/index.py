"""Context generator"""
from pathlib import Path
from random import choice
from typing import Mapping, MutableMapping, Sequence

from website.pages._page import Page


class Index(Page, url="index.html"):
    """Context generator"""

    @classmethod
    def get_context(cls, request_data: Mapping) -> Mapping:
        """Return the dictionary with the data used to populate the template"""
        context = {"image": Image.get_image_from(request_data["topic"])}
        return context


class Image:
    """Singleton to access images"""

    _SERVER_DIR = Path(__file__).parent.parent
    _IMAGE_DIR = "static/img/topic"
    _cache: MutableMapping = {}

    @classmethod
    def get_image_from(cls, topic: str) -> str:
        """Returns a random image from the directory"""
        images = cls.get_image_list_from(topic)
        image = choice(images)
        return image

    @classmethod
    def get_image_list_from(cls, topic: str) -> Sequence[str]:
        """Returns the list of images for a directory"""
        if topic not in cls._cache.keys():
            cls.refresh_image_list_from(topic)
        images = cls._cache[topic]
        print(f"{cls._IMAGE_DIR}")
        return images

    @classmethod
    def refresh_image_list_from(cls, topic: str) -> None:
        """Retrieve the list of images for a directory"""
        cls._cache[topic] = []
        for filepath in (cls._SERVER_DIR / cls._IMAGE_DIR / topic).iterdir():
            cls._cache[topic].append(filepath.relative_to(cls._SERVER_DIR))
        cls._cache[topic].sort()
