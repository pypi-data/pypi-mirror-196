from flask import Flask
from flask.cli import AppGroup

from flask_cblueprint.commands.create_blueprint import create_blueprint_command
from flask_cblueprint.commands.list_blueprint import list_blueprints_command

# > This class is a blueprint for the Flask CLI
class FlaskCBlueprint:
    def __init__(self, app: Flask | None = None) -> None:
        
        # Creating a new CLI command called `app`.
        self.__app_cli: AppGroup = AppGroup('app')

        # A way to make the class more flexible.
        # If you want to use the class without passing an app,
        # you can do it.
        # But if you want to pass an app, you can do it too.
        # It is a way to make the class more flexible.
        if app is not None:
            self.init_app(app)

    def __add_command(self):
        """
        It adds the commands to the app's command line interface
        """
        self.__app_cli.add_command(create_blueprint_command)
        self.__app_cli.add_command(list_blueprints_command)

    def init_app(self, app: Flask) -> None:
        """
        It adds a command to the Flask CLI.
        
        :param app: Flask
        :type app: Flask
        """
        # A way to make the class more flexible.
        # If you want to use the class without passing an app,
        # you can do it.
        # But if you want to pass an app, you can do it too.
        # It is a way to make the class more flexible.
        blueprint_directories = app.config.setdefault('FLASK_CBLUEPRINTS_DIRECTORY', None)
        if blueprint_directories is None:
            blueprint_directories = 'app/blueprints'

        # Updating the app's configuration.
        app.config.update(
            FLASK_CBLUEPRINTS_DIRECTORY = blueprint_directories
        )
        # Adding the commands to the app's command line interface.
        self.__add_command()
        app.cli.add_command(self.__app_cli)
