"""Context generator"""
from json import dumps
from pathlib import Path
from random import shuffle
from typing import Mapping, MutableMapping, Sequence

from website.pages._page import Page

SERVER_DIR = Path(__file__).parent.parent
IMAGE_DIR = "static/img/topic"


class Images(Page, url="images.json"):
    """Context generator"""

    @classmethod
    def get_context(cls, request_data: Mapping) -> Mapping:
        """Return the dictionary with the data used to populate the template"""
        data = cls.get_images(request_data["topic"])
        context = {"data": dumps(data)}
        return context

    @classmethod
    def get_images(cls, topic: str) -> Mapping:
        """Return a shuffled list of all the images

        :param topic: topic to pull the filename from.

        :return: A map with the image attributes.
        """
        images = Image.get_images_from(topic)
        data = {
            "images": [
                {
                    "filename": f.name,
                    "url": f"/{f.relative_to(SERVER_DIR)}",
                }
                for f in images
            ]
        }
        shuffle(data["images"])
        return data


class Image:
    """Singleton to access images"""

    _cache: MutableMapping[str, Sequence[Path]] = {}

    @classmethod
    def get_images_from(cls, topic: str) -> Sequence:
        """Returns a random image from the directory"""
        images = cls.get_image_list_from(topic)
        return images

    @classmethod
    def get_image_list_from(cls, topic: str) -> Sequence[Path]:
        """Returns the list of images for a directory"""
        if topic not in cls._cache.keys():
            cls.refresh_image_list_from(topic)
        images = cls._cache[topic]
        return list(images)

    @classmethod
    def refresh_image_list_from(cls, topic: str) -> None:
        """Retrieve the list of images for a directory"""
        images = [
            f.absolute()
            for f in (SERVER_DIR / IMAGE_DIR / topic).iterdir()
            if not f.name.startswith(".")
        ]
        images.sort()
        cls._cache[topic] = images
