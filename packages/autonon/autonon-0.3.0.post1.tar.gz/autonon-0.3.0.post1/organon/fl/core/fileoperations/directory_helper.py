"""
This module keeps the get_current_directory function.
"""
import os


def get_current_directory() -> str:
    """
    Returns the current working directory path.
    :return: current working directory path
    """
    path = os.getcwd()
    return path


def get_name(path: str) -> str:
    """
    Returns the name of the file in the given path
    :return: name of the file in the given path
    """
    return os.path.basename(path)


def exists(path: str) -> bool:
    """
    Returns True if given path exists
    """
    return os.path.isdir(path)


def create(path: str, exception_if_exists: bool = False):
    """
    Creates directories and subdirectories for given path
    """
    os.makedirs(path, exist_ok=not exception_if_exists)
