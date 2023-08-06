from pathlib import Path

from PIL.IcnsImagePlugin import IcnsFile


def icon_sizes(filepath: Path):
    """Return the sizes of the icons in an icns file."""
    with filepath.open("rb") as fp:
        imf = IcnsFile(fp)
        sizes = imf.itersizes()
        return sizes


def read_icon(filepath: Path, size=None):
    """Load an icon from a file."""
    with filepath.open("rb") as fp:
        imf = IcnsFile(fp)
        im = imf.getimage(size)
        im.load()
        return im
