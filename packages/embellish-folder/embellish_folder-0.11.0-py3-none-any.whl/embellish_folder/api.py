import tempfile
from pathlib import Path

from embellish_folder.base_icons import compose_icon
from embellish_folder.fileicon import set_icon, clear_icon

DEFAULT_ICONS_FILEPATH = Path("/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/GenericFolderIcon.icns")



def embellish_folder(folder_path: Path | str, embellishment_path: Path | str):
    """Embellish a folder with a custom icon.

    Args:
        folder_path: The path to the folder to embellish.

        embellishment_path: The path to the image with which to embellish the folder icon.

    Raises:
        NotADirectoryError: If the folder path does not exist or is not a directory.
        RuntimeError: If the fileicon command line tool is not available or if it fails to set.
    """
    folder_path = Path(folder_path)
    embellishment_path = Path(embellishment_path)
    if folder_path.is_file():
        raise NotADirectoryError(f"Folder path is not a directory: {folder_path}")
    if not folder_path.is_dir():
        raise FileNotFoundError(f"Folder path does not exist: {folder_path}")

    # Make a temporary filename available for the icon in a context manager
    with tempfile.NamedTemporaryFile(suffix='.icns') as icns_file:
        icns_path = Path(icns_file.name)
        compose_icon(embellishment_path, DEFAULT_ICONS_FILEPATH, icns_path)
        set_icon(folder_path, icns_path)


def remove_embellishment(folder_path):
    """Remove the embellishment from a folder.

    Args:
        folder_path: The path to the folder from which to remove the embellishment.

    Raises:
        RuntimeError: If the fileicon command line tool is not available or if it fails to clear.
    """
    folder_path = Path(folder_path)
    clear_icon(folder_path)


if __name__ == '__main__':
    # This is just for testing
    embellish_folder(
        "/Users/rjs/Code/embellish-folder/tests/data/t5",
        "/Users/rjs/Code/embellish-folder/tests/data/terminal-800x600.png",
    )