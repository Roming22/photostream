#!/usr/bin/env python3
"""Routing module

Should contain nothing but routing information
"""
import os
import sys
from traceback import format_exception
from typing import Any, Mapping, MutableMapping

from flask import Flask, abort, request
from flask.logging import create_logger
from markupsafe import escape

from website.pages import render as render_page

APP = Flask(__name__)
LOGGER = create_logger(APP)


@APP.route("/<topic>")
def index(topic: str) -> str:  # pylint: disable=inconsistent-return-statements
    """Website homepage"""
    request_data = {"topic": escape(topic)}
    return render("topic.html", request_data)


@APP.route("/<topic>/<name>", methods=["GET", "DELETE"])
def filename(
    topic: str, name: str
) -> str:  # pylint: disable=inconsistent-return-statements
    """Get image URL"""
    request_data: MutableMapping[str, Any] = {
        "topic": escape(topic),
        "filename": escape(name),
        "http_method": request.method,
    }
    return render("filename.json", request_data)


@APP.route("/")
def root() -> str:
    """Service entry-point"""
    return render("index.html", {})


def render(url: str, request_data: Mapping) -> str:
    """Generic function to render a page"""
    context = {"url_prefix": ""}
    if "KUBERNETES_PORT" in os.environ.keys():
        service = request.host.split(":")[0]
        context["url_prefix"] = f"/{service}"
    try:
        response = render_page(url, request_data, context)
    except Exception as ex:  # pylint: disable=broad-except
        message = f"Unexpected Exception: {ex}"
        LOGGER.info("".join(format_exception(*sys.exc_info())))
        LOGGER.error(message)
        abort(500, message)
    return response
