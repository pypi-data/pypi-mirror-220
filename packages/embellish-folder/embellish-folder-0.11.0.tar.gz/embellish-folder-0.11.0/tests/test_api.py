from pathlib import Path

import pytest

from embellish_folder import api

@pytest.fixture
def folder_path(tmp_path) -> Path:
    path = tmp_path / "folder"
    path.mkdir()
    return path


def test_embellish_folder_with_no_such_folder_raises_file_not_found_error():
    with pytest.raises(FileNotFoundError, match="Folder path does not exist: no-such-folder"):
        api.embellish_folder("no-such-folder", "tests/data/embellishment.png")


def test_embellish_folder_with_file_path_for_folder_raises_not_a_directory_error():
    with pytest.raises(NotADirectoryError, match="Folder path is not a directory: tests/data/embellishment.png"):
        api.embellish_folder("tests/data/embellishment.png", "tests/data/embellishment.png")


def test_embellish_folder_with_no_such_image_file_raises_file_not_found_error(folder_path: Path):
    with pytest.raises(FileNotFoundError, match="No such file or directory"):
        api.embellish_folder(folder_path, "no-such-image.png")
