# It's importing the modules that we need to use in our functions.
import os
import glob
import shutil

from pathlib import Path
from string import Template


def create_folder_if_not(folder_path):
    """
    If the folder path doesn't exist, create it
    
    :param folder_path: The path to the folder you want to create
    :return: the path to the folder.
    """
    return os.makedirs(os.path.dirname(folder_path), exist_ok=True)


def list_files(directory, **kwargs):
    """
    "Return a list of files in a directory, ignoring files in the ignore list and optionally only
    returning files with a specific file extension."
    
    The function takes two arguments:
    
    directory: The directory to list files from.
    ignore: A list of files to ignore.
    The function also takes two keyword arguments:
    
    file_extension: A file extension to filter files by.
    ignore: A list of files to ignore.
    The function returns a list of files
    
    :param directory: The directory to list files from
    :return: A list of files in the directory.
    """
    ignore = kwargs.get("ignore", [""])
    file_extension = kwargs.get("file_extension")

    files = []

    # It's iterating through the files in the directory, and if the file is not in the ignore list,
    # it appends the file to the files list.
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            if file not in ignore:
                if file_extension and file.endswith(file_extension):
                    files.append(file)

                elif not file_extension:
                    files.append(file)

    return files


def list_directories(directory, ignore=None):
    """
    It returns a list of directories in a given directory, ignoring any directories in the ignore list
    
    :param directory: The directory to list the contents of
    :param ignore: A list of directories to ignore
    :return: A list of directories in the given directory.
    """
    if not ignore:
        ignore = ["__pycache__"]

    return list(
        filter(
            lambda x: os.path.isdir(os.path.join(directory, x)) and x not in ignore,
            os.listdir(directory)
        )
    )


def set_file(file_path, file_content):
    """
    It opens a file, writes to it, and closes it
    
    :param file_path: The path to the file you want to write to
    :param file_content: The content of the file you want to write to
    """
    with open(file_path, 'w') as f:
        f.write(file_content)
        f.close()


def has_file(file_path):
    """
    `has_file` takes a file path as a string and returns a boolean indicating whether or not the file
    exists.
    
    :param file_path: The path to the file you want to check
    :return: A boolean value.
    """
    # It's creating a path object from the file path.
    potential_file = Path(file_path)

    return potential_file.is_file()


def copy_file(src, dest):
    """
    "Copy the file at the path src to the path dest."
    
    The function takes two arguments, src and dest, and returns the result of shutil.copy(src, dest)
    
    :param src: The source file path
    :param dest: The destination path where the file is to be copied
    :return: The return value is the path to the newly created file.
    """
    return shutil.copy(src, dest)


def read_file(file_path):
    """
    "This function takes a file path and returns a file object."
    
    The first line of the function is called the docstring. It's a special comment that describes what
    the function does
    
    :param file_path: The path to the file you want to read
    :return: The file object
    """
    return open(file_path, 'r')


def replace_templates_in_files(lookup_path, file_extension, template_vars, ignore=None):
    """
    It takes a path, a file extension, a dictionary of template variables, and an optional list of files
    to ignore, and then it replaces all the template variables in all the files in the path with the
    file extension
    
    :param lookup_path: The path to the directory where the files are located
    :param file_extension: The file extension of the files you want to replace the templates in
    :param template_vars: A dictionary of variables to replace in the template files
    :param ignore: A list of files to ignore
    """
    if not ignore:
        ignore = []

    # Using the glob module to find all the files in the lookup_path with the file_extension
    files = [f for f in glob.glob(lookup_path + "/**/*%s" % file_extension, recursive=True)]

    # Iterating through the files in the files list, and if the file is not in the ignore list, it
    # opens the file, reads the file, and then closes the file. Then it opens the file again, writes
    # the file, and then closes the file.
    for f in files:
        if f.split("/")[-1] not in ignore:
            file = open(f, 'r')
            file_content = Template(file.read()).substitute(template_vars)
            file.close()

            file = open(f, 'w')
            file.write(file_content)
            file.close()
