import os
from glob import glob
import yaml
from collections import OrderedDict
import requests
import toml
from pathlib import Path
from typing import Callable, Optional



def check_or_create_subdirectory(directory: str, subdirectory: str, callback: Callable[[str], None]) -> None:
    """
    Checks if a subdirectory exists within a specified directory. If the subdirectory does not exist, it is created.
    The callback function is then called with a message indicating whether the subdirectory was created or already existed.
    
    Args:
        directory (str): The absolute or relative path of the parent directory.
        subdirectory (str): The name of the subdirectory to be checked/created.
        callback (Callable[[str], None]): A callback function that accepts a string message as an argument. 
                                          This function is called after the check/create operation with a message 
                                          indicating whether the subdirectory was created or already existed.
        
    Returns:
        None
        
    Raises:
        OSError: If the directory cannot be created due to a system-related error (like lack of permissions, 
                 or the parent directory not existing)
    
    Usage:
        def callback_function(message: str) -> None:
            print(message)

        check_or_create_subdirectory('/path/to/directory', 'new_subdirectory', callback_function)

    """
    try:
        subdirectory_path = os.path.join(directory, subdirectory)
        os.makedirs(subdirectory_path, exist_ok=True)
        
        if os.path.isdir(subdirectory_path):
            callback(f"The subdirectory '{subdirectory}' already exists at: {subdirectory_path}")
        else:
            callback(f"The subdirectory '{subdirectory}' was created at: {subdirectory_path}")
    except OSError as e:
        callback(f"Could not create the subdirectory '{subdirectory}' at: {subdirectory_path}. Error: {str(e)}")


def callback_function(message: str) -> None:
    print(message)


def get_files_dictionary(dirpath: str, file_extension: str, keep_extension_in_key:bool = False) -> dict:
    """
    Recursively search for files with the specified `file_extension` in the given `dirpath` and return a dictionary
    with the filename (without extension) as the key and the full normalized path of the file as the value.

    Args:
        dirpath (str): The directory path to start the search.
        file_extension (str): The file extension to filter the files.
        keep_extension_in_key (bool, optional): If True, the file extension will be kept in the key of the dictionary.

    Returns:
        dict: A dictionary where the keys are the filenames (without extension) and the values are the full normalized paths of the files.
    """
    if not os.path.isdir(dirpath):
        raise ValueError(f"The specified directory path '{dirpath}' does not exist or is not a directory.")

    files_dictionary = {}
    
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith(file_extension):
                full_path = os.path.join(root, file)
                if keep_extension_in_key:
                    files_dictionary[file] = os.path.normpath(full_path)
                else:
                    filename_without_extension = os.path.splitext(file)[0]
                    files_dictionary[filename_without_extension] = os.path.normpath(full_path)

    return files_dictionary


def create_directory_list(dirpath: str) -> list:
    """
    Creates a list of directories within a given directory, excluding files.

    Args:
        dirpath (str): The path of the directory.

    Returns:
        list: A list of directories within the given directory.

    Raises:
        OSError: If there is an error accessing the directory.
    """
    try:
        directories = []
        for item in os.listdir(dirpath):
            item_path = os.path.join(dirpath, item)
            if os.path.isdir(item_path):
                directories.append(item_path)
        return directories
    except OSError as e:
        raise OSError(f"Error accessing directory: {e}")


def create_file_list_with_extension(dirpath: str, extension: str) -> list:
    """
    Creates a list of files within a given directory, filtered by file extension.

    Args:
        dirpath (str): The path of the directory.
        extension (str): The file extension to filter by (e.g., ".txt", ".csv").

    Returns:
        list: A list of file paths within the given directory that match the specified file extension.

    Raises:
        OSError: If there is an error accessing the directory.
    """
    try:
        files = []
        for item in os.listdir(dirpath):
            item_path = os.path.join(dirpath, item)
            if os.path.isfile(item_path) and item.endswith(extension):
                files.append(item_path)
        return files
    except OSError as e:
        raise OSError(f"Error accessing directory: {e}")


def check_dirpath_owner(dirpath: str):
    """
    Checks the ownership of a directory.

    Args:
        dirpath (str): The path of the directory to check ownership for.

    Returns:
        dict: A dictionary containing the owner and group of the directory if it exists, otherwise an empty dictionary.
    """
    path = Path(dirpath)

    if path.exists():
        return {"Owner": path.owner(), "Group": path.group()}
    else:
        return {}


def check_directory_exist_and_writable(dirpath, callback=None):
    """
    Checks if a directory exists and if it is writable.

    Args:
        dirpath (str): The path of the directory to be checked.
        callback (Optional[Callable[[str], None]], optional): A callback function 
        to be executed after checking the directory. The callback function 
        should accept a single string argument, which will be a status message.

    Returns:
        success (Optional[bool]): True if the directory exists and is writable,
        False if the directory exists but is not writable, None if the directory doesn't exist.
    """
    success = None
    message = None

    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        # Check if directory exists

        if os.access(dirpath, os.W_OK):
            # Check if directory is writable

            message = f"The directory {dirpath} exists and is writable."
            success = True

        else:
            ownership = check_dirpath_owner(dirpath)
            # Get directory ownership

            message = f"The directory {dirpath} exists but is not writable. Ownership: `{ownership}`"
            success = False

    else:
        message = f"The directory {dirpath} does not exist."
        success = None

    if callback:
        callback(message)

    return success


def create_new_directory(dirpath, callback: Optional[Callable[[str], None]] = None):
    """
    Creates a new directory if it does not exist already.

    Args:
        dirpath (str): The path of the directory to be created.
        callback (Optional[Callable[[str], None]], optional): A callback function 
        to be executed after directory creation. The callback function 
        should accept a single string argument, which will be a status message.

    Returns:
        str: The path of the directory.

    Raises:
        OSError: If there is an error while creating the directory.
    """
    try:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)  # Create the directory if it doesn't exist
            message = f"The directory {dirpath} was created."
        else:
            message = f"The directory {dirpath} already exists."
    
    except OSError as e:
        raise OSError(f"Error creating directory: {e}")
    
    if callback:
        callback(message)
    
    return dirpath


def create_subdirectory(directory: str, subdirectory: str, callback: Optional[Callable[[str], None]] = None) -> str:
    """
    **depreciation warning**: Use check_or_create_subdirectory instead.
    
    Check if a subdirectory exists within a given directory and create it if it doesn't exist.
    
    The function raises exceptions if the provided directory path is invalid or 
    if there's an error while creating the subdirectory. After the subdirectory is 
    successfully created or if it already exists, a callback function can be executed 
    with a status message as its argument.

    Args:
        directory (str): Path to the directory to check/create the subdirectory in.
        subdirectory (str): Name of the subdirectory to check/create.
        callback (Optional[Callable[[str], None]], optional): A callback function 
        to be executed after creating the subdirectory. The callback function 
        should accept a single string argument, which will be a status message.
        Defaults to None.

    Returns:
        str: The full path to the subdirectory.

    Raises:
        ValueError: If the provided directory path is invalid.
        OSError: If there is an error while creating the subdirectory.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"'{directory}' is not a valid directory path.")

    subdirectory_path = os.path.join(directory, subdirectory)

    try:
        if not os.path.exists(subdirectory_path):
            os.makedirs(subdirectory_path)
            message = f"Subdirectory '{subdirectory}' created in '{directory}'."
        else:
            message = f"Subdirectory '{subdirectory}' already exists in '{directory}'."
    except OSError as e:
        message = f"Error while creating the subdirectory: {str(e)}"
        raise OSError(message) from e

    if callback:
        callback(message)

    return subdirectory_path


def load_toml_variables(file_path: str) -> dict:
    """
    Load variables from a .toml file into a dictionary.

    Args:
        file_path (str): Path to the .toml file.

    Returns:
        dict: Dictionary containing the loaded variables.

    Raises:
        IOError: If there is an error while loading the .toml file.
    """
    try:
        with open(file_path, "r") as file:
            data = toml.load(file)
            return data
    except IOError:
        raise IOError(f"Error: Unable to load .toml file from {file_path}")
        return {}


def load_yaml(filepath: str) -> dict:
    """
    Loads a YAML file.

    Can be used as stand-alone script by providing a command-line argument:
        python load_yaml.py --filepath /file/path/to/filename.yaml
        python load_yaml.py --filepath http://example.com/path/to/filename.yaml

    Args:
        filepath (str): The absolute path to the YAML file or a URL to the YAML file.

    Returns:
        dict: The contents of the YAML file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If there is an error while loading the YAML file.
    """
    if filepath.startswith('http://') or filepath.startswith('https://'):
        try:
            response = requests.get(filepath)
            response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
            yaml_data = yaml.safe_load(response.text)
        except (requests.RequestException, yaml.YAMLError) as e:
            raise Exception(f'Error loading YAML from `{filepath}`. \n {str(e)}')
        else:
            return yaml_data
    else:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"No such file or directory: '{filepath}'")

        with open(filepath, 'r') as file_descriptor:
            try:
                yaml_data = yaml.safe_load(file_descriptor)
            except yaml.YAMLError as msg:
                raise yaml.YAMLError(f'File `{filepath}` loading error. \n {msg}')
            else:
                return yaml_data


def load_yaml_from_file(file):
    """
    Loads YAML data from a file object.

    Args:
        file: The file object representing the YAML file.

    Returns:
        dict: The loaded YAML data.

    Raises:
        yaml.YAMLError: If there is an error while loading the YAML data from the file.
    """
    try:
        yaml_data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f'File loading error. \n {e}')
    else:
        return yaml_data


def get_available_services(services_filepath: str) -> OrderedDict:
    """
    Retrieves available services from a yaml file. These services can be used to
    create a multi-page app using Streamlit. 

    Args:
        services_filepath (str): The absolute path to the yaml file containing the services.

    Returns:
        OrderedDict: An ordered dictionary of services if any are available. 
                     The dictionary is ordered based on the order of services in the yaml file.
                     Each key-value pair corresponds to a service name and its associated information.
                     Returns None if the yaml file does not contain any services.
    Raises:
        FileNotFoundError: If the services_filepath does not exist.
    """
    if not os.path.isfile(services_filepath):
        raise FileNotFoundError(f"No such file or directory: '{services_filepath}'")

    available_services = load_yaml(filepath=os.path.abspath(services_filepath))

    if available_services:
        services_dict = OrderedDict({service['name']: service for service in available_services})
        return services_dict

    return None


def path_exists(path, path_type):
    """
    Checks if a given path exists, whether it's a local file, remote URL, or LAN path.

    Args:
        path (str): The path to check.
        path_type (str): The type of the path. It can be "local", "remote", or "lan".

    Returns:
        bool: True if the path exists, False otherwise.
    """
    if path_type == "remote":
        return is_remote_url(path)
    elif path_type == "lan":
        return is_lan_path(path)
    else:
        return os.path.exists(path)


def is_remote_url(path):
    """
    Checks if the given path is a remote URL.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a remote URL, False otherwise.
    """
    return path.startswith('http://') or path.startswith('https://')


def is_lan_path(path):
    """
    Checks if the given path is a LAN path.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a LAN path, False otherwise.
    """
    return path.startswith(os.sep + os.sep)
