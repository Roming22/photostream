#!/usr/bin/env python3
"""Routing module

Should contain nothing but routing information
"""
import sys
from traceback import format_exception
from typing import Any, Mapping, MutableMapping

from flask import Flask, abort, request
from flask.logging import create_logger

from website.pages import render as render_page

APP = Flask(__name__)
LOGGER = create_logger(APP)


@APP.route("/<topic>")
def index(topic: str) -> str:  # pylint: disable=inconsistent-return-statements
    """Website homepage"""
    request_data = {"topic": topic}
    return render("topic.html", request_data)


@APP.route("/<topic>/images", methods=["GET"])
def images(topic: str) -> str:  # pylint: disable=inconsistent-return-statements
    """Get image URL"""
    request_data: MutableMapping[str, Any] = {"topic": topic}
    return render("images.json", request_data)


@APP.route("/<topic>/file/<name>", methods=["DELETE"])
def image(
    topic: str, name: str
) -> str:  # pylint: disable=inconsistent-return-statements
    """Delete image"""
    request_data: MutableMapping[str, Any] = {
        "topic": topic,
        "filename": name,
        "http_method": request.method,
    }
    return render("file.json", request_data)


@APP.route("/")
def root() -> str:
    """Service entry-point"""
    return render("index.html", {})


def render(url: str, request_data: Mapping) -> str:
    """Generic function to render a page"""
    try:
        response = render_page(url, request_data)
    except Exception as ex:  # pylint: disable=broad-except
        message = f"Unexpected Exception: {ex}"
        LOGGER.info("".join(format_exception(*sys.exc_info())))
        LOGGER.error(message)
        abort(500, message)
    return response
