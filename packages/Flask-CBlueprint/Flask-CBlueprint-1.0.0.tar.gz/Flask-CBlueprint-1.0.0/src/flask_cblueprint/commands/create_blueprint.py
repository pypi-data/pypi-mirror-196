import click
import os
import shutil
from string import Template
from simple_term_menu import TerminalMenu

from flask.cli import with_appcontext
from flask import current_app

from flask_cblueprint.utils.list import list_boilerplate_skeletons
from flask_cblueprint.utils.validate import validate_name
from flask_cblueprint.utils import filesystem
from flask_cblueprint.utils.list import list_boilerplate_models
from flask_cblueprint.utils.string import snake_to_camel
from flask_cblueprint.config import BLUEPRINTS_BOILERPLATE, BLUEPRINTS_VIEW_STYLES, FLASK_LINK_VIEWS


@click.command('create-blueprint')
@click.option('--app-name', help='app name', prompt='Enter you app name', callback=validate_name, default='app')
@click.option('--name', help='Blueprint name', prompt='Enter blueprint name', callback=validate_name)
@click.option('--create-model', is_flag=True, prompt='Create default model?', default=True,
              show_default=True, help='Use, if you need empty model')
@click.option('--url-rule', prompt='Set your initial url rule', help='Set initial url rule [Example: /hello_world]', default='/')
@click.option('--skeleton', help='Skeleton name (folder name)')
@with_appcontext
def create_blueprint_command(app_name, name, create_model, url_rule, skeleton):
    """
    > It creates a blueprint folder structure, creates a model if requested, and injects template
    variables into the blueprint files
    
    :param app_name: The name of the app
    :param name: The name of the blueprint
    :param create_model: If True, a model will be created for the blueprint
    :param url_rule: The URL rule for the blueprint
    :param skeleton: The blueprint structure
    """
    available_view_styles = BLUEPRINTS_VIEW_STYLES
    available_skeletons = list_boilerplate_skeletons(BLUEPRINTS_BOILERPLATE)

    # Creating a menu for the user to select a skeleton.
    if not skeleton:
        skeleton_selection_menu = TerminalMenu(
            available_skeletons,
            title="Select skeleton (Your future blueprint structure)"
        )
        skeleton = available_skeletons[skeleton_selection_menu.show()]
    
    # Printing the skeleton name to the console.
    click.echo(f"Skeleton: {skeleton}")

    # Creating a menu for the user to select a view style.
    view_style_selection_menu = TerminalMenu(
        list(map(lambda x: x[0], available_view_styles)),
        title=f"Select view style. {FLASK_LINK_VIEWS}"
    )
    view_style_index = view_style_selection_menu.show()
    view_style = available_view_styles[view_style_index]
    click.echo("View style: %s" % view_style[0])

    # create_blueprint(skeleton, app_name, view_style, name, create_model, url_rule)
    def echo_success(msg):
        click.echo(click.style(msg, fg="green", bold=True))

    # 
    available_models = list_boilerplate_models(BLUEPRINTS_BOILERPLATE)
    boilerplate_folder = BLUEPRINTS_BOILERPLATE
    blueprints_folder = current_app.config['FLASK_CBLUEPRINTS_DIRECTORY']
    view_style_folder = view_style[1]

    # Creating a dictionary with the keys and values of the variables that will be used in the
    # templates.
    template_vars = {
        **{
            "app_name": app_name,
            "model_name": "%sModel" % snake_to_camel(name),
            "view_name": "%sView" % snake_to_camel(name),
            "view_name_api": "%sAPI" % snake_to_camel(name),
            "blueprint_name": name,
            "blueprint_name_camelcase": snake_to_camel(name),
            "blueprint_name_route": "%s_route" % name,
            "url_rule": url_rule
        },
    }

    # 1: Create blueprint structure
    dest_path = os.path.join(os.getcwd(), blueprints_folder, name)
    shutil.copytree(
        os.path.join(boilerplate_folder + "/skeletons", skeleton),
        dest_path
    )
    echo_success("[x] Structure created.")

    # 2: Create model
    if create_model:
        model_selection_menu = TerminalMenu(
            available_models,
            title="Select future model template"
        )
        model_template = available_models[model_selection_menu.show()]

        with open('%s/models/%s' % (boilerplate_folder, model_template), 'r') as f:
            model_text = Template(f.read()).substitute(template_vars)

        filesystem.set_file("%s/models/%s.py" % (dest_path, name), model_text)

        echo_success("[x] Model created")

    else:
        click.echo(click.style("[ ] Model not selected and ignored.", fg="cyan"))

    # 3: Modify files according to view_style
    if view_style_folder:
        view_template = view_style_folder + "/view.py.template"
        routes_template = view_style_folder + "/routes.py.template"

        if filesystem.has_file(view_template):
            view_script = open(view_template, "r")
            filesystem.set_file("%s/views/%s.py" % (dest_path, name), view_script.read())

        if filesystem.has_file(routes_template):
            routes_script = open(routes_template, "r")
            filesystem.set_file("%s/routes.py" % dest_path, routes_script.read())

        echo_success("[x] View style updated according to %s" % view_style[0])

    else:
        click.echo(click.style("[ ] View style not selected and ignored.", fg="cyan"))

    # 4: Replace string templates in .py files
    filesystem.replace_templates_in_files(dest_path, ".py", template_vars, ["__init__.py"])

    echo_success("[x] Template variables injected.")
    echo_success("All done. Now you can start customizing your newly created blueprint.")