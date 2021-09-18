#!/usr/bin/env python3
"""Main module

CLI to control the server
Should contain nothing but the bootstrapping code to start the server
"""
import os
from functools import partial

import click
from waitress import serve

from website.__version__ import __commit__, __version__
from website.routing import APP


@click.command()
@click.option(
    "--dev",
    "-d",
    is_flag=True,
    help="If true run the flask server in development mode",
)
def cli(dev: bool) -> None:
    """Start the server

    The environment is different in local test vs prod, mostly because of the web server
    used to serve the application.
    """
    print(f"photostream {__version__} ({__commit__})")
    os.environ["FLASK_APP"] = "main"

    if dev:
        # Do not use those settings in production.
        os.environ["FLASK_DEBUG"] = "1"
        os.environ["FLASK_ENV"] = "development"
        server = APP.run
    else:
        server = partial(serve, APP)
    server(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
