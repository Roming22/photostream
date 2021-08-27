"""Main module

Should contain nothing but routing information
"""
import sys
from traceback import format_exception
from typing import Mapping

from flask import Flask, abort
from flask.logging import create_logger

from website.pages import render as render_page

APP = Flask(__name__)
LOGGER = create_logger(APP)


@APP.route("/")
def index() -> str:  # pylint: disable=inconsistent-return-statements
    """Website homepage"""
    return render("index.html")


@APP.route("/alive")
def alive() -> Mapping:
    """Service entry-point

    Used by OCP to check that the service is started"""
    return {}


def render(url: str) -> str:
    """Generic function to render a page"""
    try:
        response = render_page(url)
    except Exception as ex:  # pylint: disable=broad-except
        message = f"Unexpected Exception: {ex}"
        LOGGER.info("".join(format_exception(*sys.exc_info())))
        LOGGER.error(message)
        abort(500, message)
    return response
