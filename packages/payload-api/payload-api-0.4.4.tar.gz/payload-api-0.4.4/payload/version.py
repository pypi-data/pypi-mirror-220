import importlib.metadata
from pathlib import Path

try:
    __version__ = importlib.metadata.version(__package__ or __name__.split(".", maxsplit=1)[0])
except importlib.metadata.PackageNotFoundError:
    with open(str(Path(__file__).parent.parent)+'/pyproject.toml') as pyproject_toml:
            __version__ = (
                next(line for line in pyproject_toml if line.startswith("version"))
                .split("=")[1]
                .strip("'\"\n ")
            )

__version__ = tuple(map(int,__version__.split('.')))
