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
    return render("index.html", request_data)


@APP.route("/<topic>/<name>", methods=["GET", "DELETE"])
def filename(
    topic: str, name: str
) -> str:  # pylint: disable=inconsistent-return-statements
    """Get image URL"""
    request_data: MutableMapping[str, Any] = {
        "topic": topic,
        "filename": name,
        "http_method": request.method,
    }
    return render("filename.json", request_data)


@APP.route("/alive")
def alive() -> Mapping:
    """Service entry-point

    Used by OCP to check that the service is started"""
    return {}


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
