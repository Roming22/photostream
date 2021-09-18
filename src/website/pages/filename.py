"""Context generator"""
from json import dumps
from pathlib import Path
from random import choice
from typing import Mapping, MutableMapping, Sequence

from website.pages._page import Page

SERVER_DIR = Path(__file__).parent.parent
IMAGE_DIR = "static/img/topic"


class Filename(Page, url="filename.json"):
    """Context generator"""

    @classmethod
    def get_context(cls, request_data: Mapping, context: MutableMapping) -> Mapping:
        """Return the dictionary with the data used to populate the template"""
        if request_data["http_method"] == "GET":
            data = cls.get_image(
                request_data["filename"], request_data["topic"], context["url_prefix"]
            )
        elif request_data["http_method"] == "DELETE":
            data = cls.delete_image(request_data["filename"], request_data["topic"])
        context["data"] = dumps(data)
        return context

    @classmethod
    def get_image(cls, filename: str, topic: str, url_prefix: str) -> Mapping:
        """Return the path to an image

        :param filename: If set to "random" a random file from the topic is returned.
        :param topic: topic to pull the filename from.

        :return: A map with the file attributes.
        """
        if filename == "random":
            filepath = Image.get_random_image_from(topic)
        else:
            filepath = SERVER_DIR / IMAGE_DIR / topic / filename
        data = {
            "filename": filepath.name,
            "filepath": f"{filepath.relative_to(SERVER_DIR)}",
            "topic": topic,
            "url": f"{url_prefix}/{filepath.relative_to(SERVER_DIR)}",
        }
        return data

    @classmethod
    def delete_image(cls, filename: str, topic: str) -> Mapping:
        """Delete an image

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


class Image:
    """Singleton to access images"""

    _cache: MutableMapping[str, Sequence[Path]] = {}

    @classmethod
    def get_random_image_from(cls, topic: str) -> Path:
        """Returns a random image from the directory"""
        images = cls.get_image_list_from(topic)
        image = choice(images)
        return image

    @classmethod
    def get_image_list_from(cls, topic: str) -> Sequence[Path]:
        """Returns the list of images for a directory"""
        if topic not in cls._cache.keys():
            cls.refresh_image_list_from(topic)
        images = cls._cache[topic]
        return images

    @classmethod
    def refresh_image_list_from(cls, topic: str) -> None:
        """Retrieve the list of images for a directory"""
        files = [f.absolute() for f in (SERVER_DIR / IMAGE_DIR / topic).iterdir()]
        files.sort()
        cls._cache[topic] = files
