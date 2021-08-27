#!/usr/bin/env python3
"""CLI to control the server"""

import os
from pathlib import Path

import click


@click.command()
@click.option(
    "--dev",
    "-d",
    is_flag=True,
    help="If true run the flask server in development mode",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="verbose mode",
)
def cli(dev: bool, verbose: bool) -> None:
    """Start the server

    The environment is different in local test vs prod, mostly because of the webserver
    used to serve the application.
    """
    if dev:
        # Do not use those settings in production.
        os.environ["FLASK_DEBUG"] = "1"
        os.environ["FLASK_ENV"] = "development"
        cmd = ["flask", "run", "--host=0.0.0.0"]
    else:
        # Waitress seems to be the simplest solution
        # c.f. https://dev.to/thetrebelcc/how-to-run-a-flask-app-over-https-using-waitress-and-nginx-2020-235c
        raise Exception("[ERROR] Use a proper webserver")
    if verbose:
        log = lambda message: print(message)
    else:
        log = lambda _: None

    website_dir = Path(__file__).absolute().parent.parent / "src/website"
    os.chdir(website_dir)
    os.environ["FLASK_APP"] = "main"
    log(f"Command: cd {Path.cwd().absolute()}; {' '.join(cmd)};")
    os.execvp(cmd[0], cmd)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
