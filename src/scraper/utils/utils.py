import shutil
from configparser import ConfigParser
from pathlib import Path


def get_config(section: str, key: str) -> str:
    """Get the config from config file.

    Args:
        section (str): The section in the config file
        key (str): The key in the section

    Returns:
        str: The configuration
    """
    curr_dir = Path(__file__).parent
    config_file_location = curr_dir.parent.parent.parent / "config.ini"

    cfg = ConfigParser()
    cfg.read(config_file_location)
    return cfg[section][key]


def get_temp_directory(
    folder: str, subfolder: str | None = None, reset: bool = False
) -> Path:
    """Create a temporary directory.

    Args:
        folder (str): The folder name
        subfolder (str | None, optional): The subfolder name. Defaults to None.
        reset (bool, optional): Whenever to delete files in the folder or subfolder
            if it exists. Defaults to False.

    Returns:
        Path: The path of the folder created
    """
    curr_dir = Path(__file__).parent
    temp_file_location = curr_dir.parent / "temp_files" / folder
    if subfolder is not None:
        temp_file_location = temp_file_location / subfolder
    if reset:
        shutil.rmtree(temp_file_location, ignore_errors=True)
    temp_file_location.mkdir(parents=True, exist_ok=True)
    return temp_file_location
