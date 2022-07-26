"""Define version."""


import pathlib
import subprocess


here = pathlib.Path(__file__).resolve().parent


__all__ = ["__version__", "__branch__"]


# read from VERSION file
with open(str(here / "VERSION")) as f:
    __version__ = f.read().strip()

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
