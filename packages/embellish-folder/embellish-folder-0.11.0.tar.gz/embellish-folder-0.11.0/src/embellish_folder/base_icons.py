from pathlib import Path

from PIL import Image, ImageDraw

from embellish_folder.read import icon_sizes, read_icon
from embellish_folder.write import write_icon


def superimpose_images(foreground: Image, background: Image):
    """Superimpose an image on the default folder icon."""
    folder_icon = background.copy()
    icon_width, icon_height = folder_icon.size
    target_region_top = 0.26 * icon_height
    target_region_bottom = 0.78 * icon_height
    target_region_padding = 0.02 * icon_height
    target_region_height = (target_region_bottom - target_region_top) - (2 * target_region_padding)
    border = 0.01 * min(icon_width, icon_height)

    size_ratio = 3/4
    ideal_thumbnail_width = round(icon_width * size_ratio)
    ideal_thumbnail_height = round(target_region_height)
    foreground.thumbnail((ideal_thumbnail_width, ideal_thumbnail_height))
    actual_thumbnail_width, actual_thumbnail_height = foreground.size

    image_x = (icon_width - actual_thumbnail_width) // 2
    image_y = int(
        target_region_top + target_region_padding + (target_region_height - actual_thumbnail_height) / 2
    )
    foreground = foreground.convert("RGBA")
    folder_icon.paste(foreground, (image_x, image_y), foreground)

    draw = ImageDraw.Draw(folder_icon)

    rx0 = image_x - border
    ry0 = image_y - border
    rx1 = image_x + actual_thumbnail_width + border
    ry1 = image_y + actual_thumbnail_height + border

    draw.rectangle(
        (rx0, ry0, rx1, ry1),
        fill=(255, 255, 255, 255),
    )

    folder_icon.paste(
        foreground,
        (image_x, image_y),
    )
    return folder_icon


def compose_icon(foreground_image_path: Path, background_icns_path: Path, output_path: Path):
    """Create a new icns file from an image and a background icns file."""
    foreground_image = Image.open(foreground_image_path)
    images = [
        superimpose_images(foreground_image, read_icon(background_icns_path, size))
        for size in icon_sizes(background_icns_path)
    ]
    with output_path.open("wb") as fp:
        write_icon(fp, images)


if __name__ == "__main__":
    from pathlib import Path
    from PIL import Image

    foreground_image_path = Path("tests/data/terminal-800x600.png")
    background_icns_path = Path("tests/data/GenericFolderIcon.icns")
    compose_icon(foreground_image_path, background_icns_path, Path("tests/data/output.icns"))

