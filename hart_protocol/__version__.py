"""Define version."""

import pathlib
import subprocess
from .VERSION import __version__


here = pathlib.Path(__file__).resolve().parent


__all__ = ["__version__", "__branch__"]

try:
    __branch__ = (
        subprocess.run(["git", "branch", "--show-current"], capture_output=True, cwd=here)
        .stdout.strip()
        .decode()
    )
except:
    __branch__ = ""

if __branch__:
    __version__ += "+" + __branch__
