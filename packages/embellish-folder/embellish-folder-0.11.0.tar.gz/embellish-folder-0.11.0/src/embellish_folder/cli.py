import logging
import signal
import sys

import click
from exit_codes import ExitCode

from embellish_folder import api

logger = logging.getLogger()

@click.group()
def cli():
    """Embellish folder icons with a thumbnail image."""
    pass


@cli.command()
@click.argument(
    "folder_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.argument(
    "embellishment_image_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
def add(folder_path, embellishment_image_path):
    """Embellish a folder's icon with a custom image."""
    try:
        api.embellish_folder(folder_path, embellishment_image_path)
    except RuntimeError as e:
        print_error(e)
        sys.exit(sys.exit(ExitCode.DATA_ERR))
    except KeyboardInterrupt as e:
        print_error(e)
        sys.exit(128 + signal.SIGINT)



@cli.command()
@click.argument(
    "folder_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
def remove(folder_path):
    """Remove the embellishment from a folder."""
    try:
        api.remove_embellishment(folder_path)
    except RuntimeError as e:
        print_error(e)
        sys.exit(sys.exit(ExitCode.DATA_ERR))
    except KeyboardInterrupt as e:
        print_error(e)
        sys.exit(128 + signal.SIGINT)


def print_error(message):
    """Display an error message to the console.

    Args:
        message: The message.

    """
    click.secho(str(message), err=True, fg="red")


def print_warning(message):
    """Display an error message to the console.

    Args:
        message: The message.

    """
    click.secho(str(message), err=True, fg="magenta")


def print_info(message):
    """Display an error message to the console.

    Args:
        message: The message.

    """
    click.secho(str(message), err=True, fg="cyan")


def main():
    return cli()


if __name__ == "__main__":
    sys.exit(main())