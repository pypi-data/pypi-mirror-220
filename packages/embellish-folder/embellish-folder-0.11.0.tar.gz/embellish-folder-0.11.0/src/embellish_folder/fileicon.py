"""A Python wrapper around the fileicon command line tool.

https://github.com/mklement0/fileicon

"""

import shutil
import subprocess
import urllib
import urllib.request
import urllib.error
import http.client
import socket

from pathlib import Path


from embellish_folder.app import cache_dirpath

FILEICON = 'fileicon'


def has_fileicon() -> Path | None:
    """Check for the fileicon command line tool."""
    try:
        subprocess.check_output([FILEICON, '--help'])
    except FileNotFoundError:
        return None
    return Path(shutil.which(FILEICON))


def fileicon_exe_path() -> Path:
    return has_fileicon() or ensure_fileicon()


def ensure_fileicon() -> Path:
    """Ensure that the fileicon command line tool is available."""
    fileicon_dirpath = cache_dirpath()
    fileicon_dirpath.mkdir(parents=True, exist_ok=True)
    local_path = fileicon_dirpath / FILEICON
    url = "https://raw.githubusercontent.com/mklement0/fileicon/stable/bin/fileicon"
    try:
        resp = urllib.request.urlopen(url)
    except (urllib.error.URLError, urllib.error.HTTPError, http.client.HTTPException, socket.error) as e:
        raise RuntimeError(f"Could not download {FILEICON} from {url} ; {e}")
    else:
        status = resp.getcode()
        if status != 200:
            raise RuntimeError(f"Could not download {FILEICON} from {url} ; status code {status}")
        with local_path.open('wb') as f:
            f.write(resp.read())
        local_path.chmod(0o755)  # Make executable
    return local_path


def set_icon(subject_path: Path, icon_path: Path, quiet: bool = True):
    """Set the icon of a file or directory on macOS.

    Args:
        subject_path: The path to the file or directory of which to set the icon.

        icon_path: The path to a square image file for the icon. This can be an image file such as
            PNG, JPEG, or an ICNS file. If an ICNS file is used, it may contain more than one icon
            size. If only one image size is provided, other required sizes will be generated
            automatically.

        quiet: If True, suppresses the output of the fileicon command line tool.

    Raises:
        RuntimeError: If the fileicon command line tool is not available or if it fails to set
            the icon.
    """
    if not subject_path.exists():
        raise ValueError(f"Subject path {subject_path} does not exist.")
    args = [fileicon_exe_path(), 'set', str(subject_path), str(icon_path)]
    if quiet:
        args.append('--quiet')
    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Could not set icon for {subject_path} to {icon_path} ; {e}")

def clear_icon(subject_path: Path, quiet: bool = True):
    """Clear the icon of a file or directory on macOS.

    Args:
        subject_path: The path to the file or directory of which to clear the icon.

        quiet: If True, suppresses the output of the fileicon command line tool.

    Raises:
        RuntimeError: If the fileicon command line tool is not available or if it fails to clear
            the icon.
    """
    args = [fileicon_exe_path(), 'clear', str(subject_path)]
    if quiet:
        args.append('--quiet')
    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Could not clear icon for {subject_path} ; {e}")


if __name__ == "__main__":
    set_icon(
        Path('/Users/rjs/Code/embellish-folder/tests/data/test-folder'),
        Path('/Users/rjs/Code/embellish-folder/tests/data/output.icns'),
    )
