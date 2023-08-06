import click
from flask import current_app
from flask.cli import with_appcontext
from flask_cblueprint.utils.list import list_blueprints


@click.command("list-blueprints")
@with_appcontext
def list_blueprints_command():
    """
    It lists all the available blueprints in the `BLUEPRINTS_DIRECTORY` directory
    """
    available_blueprints = list_blueprints(current_app.config['FLASK_CBLUEPRINTS_DIRECTORY'])

    [click.echo(bp_name) for bp_name in available_blueprints]
