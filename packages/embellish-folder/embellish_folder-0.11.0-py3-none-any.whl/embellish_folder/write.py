import struct
from io import BytesIO
from typing import Iterable

from PIL.Image import Image

CODE_KEY = "type"
SIZE_KEY = "size"
STREAM_KEY = "stream"
MAGIC = b"icns"
NUM_HEADER_BYTES = 8
CODE_TO_WIDTH = {
    b"ic07": 128,
    b"ic08": 256,
    b"ic09": 512,
    b"ic10": 1024,
    b"ic11": 32,
    b"ic12": 64,
    b"ic13": 256,
    b"ic14": 512,
}


def write_icon(fp, images: Iterable[Image]):
    """
    Saves the image as a series of PNG files,
    that are then combined into a .icns file.
    """
    if hasattr(fp, "flush"):
        fp.flush()

    if not all(im.size[0] == im.size[1] for im in images):
        raise ValueError("All icons images must be square.")

    width_to_image = {im.width: im for im in images}
    largest_image_width = max(width_to_image.keys())
    largest_image = width_to_image[largest_image_width]
    width_to_stream = {}
    for size in set(CODE_TO_WIDTH.values()):
        image = (
            width_to_image[size]
            if size in width_to_image
            else largest_image.resize((size, size))
        )

        temp = BytesIO()
        image.save(temp, "png")
        width_to_stream[size] = temp.getvalue()

    entries = []
    for code, size in CODE_TO_WIDTH.items():
        stream = width_to_stream[size]
        entries.append(
            {
                CODE_KEY: code,
                SIZE_KEY: NUM_HEADER_BYTES + len(stream),
                STREAM_KEY: stream
            }
        )

    write_header(fp, entries)
    write_table_of_contents(fp, entries)
    write_images(fp, entries)

    if hasattr(fp, "flush"):
        fp.flush()


def write_images(
    fp,
    entries
):
    for entry in entries:
        fp.write(entry[CODE_KEY])
        fp.write(struct.pack(">i", entry[SIZE_KEY]))
        fp.write(entry[STREAM_KEY])


def write_table_of_contents(
    fp,
    entries
):
    fp.write(b"TOC ")
    fp.write(struct.pack(">i", NUM_HEADER_BYTES + len(entries) * NUM_HEADER_BYTES))
    for entry in entries:
        fp.write(entry[CODE_KEY])
        fp.write(struct.pack(">i", entry[SIZE_KEY]))


def write_header(
    fp,
    entries
):
    fp.write(MAGIC)
    file_length = NUM_HEADER_BYTES  # Header
    file_length += NUM_HEADER_BYTES + 8 * len(entries)  # TOC
    file_length += sum(entry[SIZE_KEY] for entry in entries)
    fp.write(struct.pack(">i", file_length))
