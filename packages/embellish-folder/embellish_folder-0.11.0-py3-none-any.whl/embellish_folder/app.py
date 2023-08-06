from pathlib import Path

from appdirs import user_cache_dir

import embellish_folder.version


def name():
    return embellish_folder.__name__


def version():
    return embellish_folder.version.__version__


def author() -> str:
    return "Robert Smallshire"


def cache_root_dirpath() -> Path:
    """The root for all caches for all visning versions."""
    return Path(user_cache_dir(name(), author()))


def cache_dirpath() -> Path:
    """A visning version-specific path for caches."""
    return cache_root_dirpath() / version()

