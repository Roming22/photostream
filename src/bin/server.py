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

    The environment is different in local test vs prod, mostly because of the web server
    used to serve the application.
    """
    cmd_env = {}
    if dev:
        # Do not use those settings in production.
        cmd_env["FLASK_DEBUG"] = "1"
        cmd_env["FLASK_ENV"] = "development"
        cmd = ["flask", "run", "--host=0.0.0.0"]
    else:
        # Waitress seems to be the simplest solution
        # c.f. https://dev.to/thetrebelcc/how-to-run-a-flask-app-over-https-using-waitress-and-nginx-2020-235c
        raise Exception("[ERROR] Use a proper webserver")
    if verbose:
        log = print
    else:

        def log(*_, **__):
            pass

    website_dir = Path(__file__).absolute().parent.parent / "website"
    os.chdir(website_dir)
    os.environ["FLASK_APP"] = "main"
    log(
        f"Command: cd {Path.cwd().absolute()}; {' '.join([f'{k}={v}' for k,v in cmd_env.items()]+cmd)};"
    )
    os.execvpe(cmd[0], cmd, dict(os.environ.items()) | cmd_env)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
