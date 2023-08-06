from flask_cblueprint.utils import filesystem

def list_blueprints(blueprints_folder, cb = None) -> list[str]:
    """
    `list_blueprints` returns a list of all the available blueprints in the given folder
    
    :param blueprints_folder: The folder where the blueprints are stored
    :param cb: A callback function that will be called for each blueprint found
    :return: A list of strings.
    """
    available_blueprints = filesystem.list_directories(blueprints_folder, ["__pycache__", "__boilerplate__"])

    # A callback function that will be called for each blueprint found
    if cb:
        for blueprint_name in available_blueprints:
            cb(blueprint_name)

    return available_blueprints

def list_boilerplate_skeletons(boilerplate_folder) -> list[str]:
    """
    "List the skeletons in the given boilerplate folder."
    
    The first line of the function is a docstring. It's a string that describes the function. It's
    optional, but it's a good idea to include it
    
    :param boilerplate_folder: The folder where the boilerplate is located
    :return: A list of strings.
    """
    return filesystem.list_directories(boilerplate_folder + "/skeletons")


def list_boilerplate_models(boilerplate_folder) -> list:
    """
    > Returns a list of all the boilerplate models in the given folder
    
    :param boilerplate_folder: The folder where the boilerplate files are stored
    :return: A list of all the files in the models folder with the extension .py.template
    """
    return filesystem.list_files(
        boilerplate_folder + "/models", file_extension="py.template")