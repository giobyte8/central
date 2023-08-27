import os


class PathCreationError(Exception):
    def __init__(self, path: str) -> None:
        Exception.__init__(self, f'Path could not be created: { path }')

class PathNotAFileError(Exception):
    def __init__(self, path: str) -> None:
        Exception.__init__(self, f'Path is not a file: { path }')

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
