from pathlib import Path


def read_files_from_parent_dir(folder_level):
    cwd = Path(__file__).parents[folder_level]
    filepath = str(cwd / "properties.json")
    return filepath


def read_store_data_txt_from_parent_dir(folder_level):
    cwd = Path(__file__).parents[folder_level]
    filepath = str(cwd / "login_methods" / ".store_data.txt")

    return filepath


def read_login_data_txt_from_parent_dir(folder_level):
    cwd = Path(__file__).parents[folder_level]
    filepath = str(cwd / "login_methods" / ".login_data.txt")
    return filepath


def read_storage_details_json_from_parent_dir(folder_level):
    cwd = Path(__file__).parents[folder_level]
    filepath = str(cwd / "storage_details.json")
    return filepath


def read_files_from_parent_dir_new(folder_level, file_name):
    """
    New function written to navigate to folder level and then find the required file name

    """
    cwd = Path(__file__).parents[folder_level]
    filepath = str(cwd / file_name)
    return filepath
