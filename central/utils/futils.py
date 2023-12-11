import os
from pathlib import Path


class PathCreationError(Exception):
    def __init__(self, path: str) -> None:
        Exception.__init__(self, f'Path could not be created: { path }')

class PathIsntFileError(Exception):
    def __init__(self, path: str) -> None:
        Exception.__init__(self, f'Path is not a valid file: { path }')

class PathNotADirectoryError(Exception):
    def __init__(self, path: str) -> None:
        Exception.__init__(self, f'Path is not a directory: { path }')


def ensure_dir_existence(path: str) -> None:
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise PathNotADirectoryError(path)
    else:
        os.makedirs(path)
        if not os.path.exists(path):
            raise PathCreationError(path)


def validate_file(path: str) -> None:
    """Verifies that given path points to a valid existent file

    Args:
        path (str): Relative or absolute path to local a file

    Raises:
        PathIsntFileError: If given path does not exists or is not a file
    """
    path = Path(path)
    if not path.is_file():
        raise PathIsntFileError(path)
