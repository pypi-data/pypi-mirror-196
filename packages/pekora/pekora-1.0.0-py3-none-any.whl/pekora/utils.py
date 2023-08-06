from __future__ import annotations

from pathlib import Path
from typing import Callable

import typer
from colour import Color
from yarl import URL

from pekora.exceptions import *
from pekora.models import *


@validate_arguments
def ninjin(term: str) -> str | int:
    """
    Convert a Pekora expression term to a Python literal.

    Pekora expression terms are:
    - Integers
    - Discord permission flags (e.g. `read_messages`)
    - Pekora permission groups (e.g. `pekora.general`)

    Parameters
    ----------
    term : str
        A valid Pekora expression term.

    Returns
    -------
        The integer value of the permission set represented by the term.

    """
    # Handle integers.
    if PekoraPattern.INTEGER.regex.match(term):
        return int(term)

    # Handle Discord permission flags.
    if term in PekoraPermissions.VALID_FLAGS:
        return PekoraPermissions.from_flags(term).value

    # Handle Pekora permission groups.
    if match := PekoraPattern.GROUP.regex.match(term):
        try:
            if isinstance(
                group := getattr(PekoraPermissions, match.group("group")), Callable
            ):
                if isinstance(permissions := group(), PekoraPermissions):
                    return permissions.value
                else:
                    raise TypeError
            else:
                raise AttributeError
        except (AttributeError, TypeError):
            raise Otsupeko(f"{term} is not a valid Pekora permission group.")

    # Handle unsupported operators.
    if PekoraPattern.UNSUPPORTED.regex.match(term):
        raise Otsupeko(f"Unsupported operator: {term}")

    # Handle other invalid input.
    raise Otsupeko(f"Invalid permission value: {term}")


def pekora_home() -> Path:
    home = Path(typer.get_app_dir("Pekora"))
    home.mkdir(exist_ok=True)
    return home


def pekora_repo() -> URL:
    return URL("https://github.com/celsiusnarhwal/pekora")


def pekora_blue() -> Color:
    return Color("#b0bfe9")


def debug_epilog() -> str:
    return "[dim]Debug mode is [green]on[/]. Turn it off with [bold cyan]pekora --debug[/]."
