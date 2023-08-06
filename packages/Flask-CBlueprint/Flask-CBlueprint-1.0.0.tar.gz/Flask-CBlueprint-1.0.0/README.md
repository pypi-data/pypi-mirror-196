### Flask-CBlueprint

is a simple extension that adds clear and basic commands to the [Flask](https://flask.palletsprojects.com/en/2.2.x/) micro framework  allowing you to easily and quickly create folder structures and [blueprints](https://flask.palletsprojects.com/en/2.2.x/api/?highlight=blueprint#flask.Blueprint).

To get started, the first thing we need to do is define where the entry point to our Flask application is located.

```bash
export FLASK_APP=sample:app OR export FLASK_APP='sample/app.py'
```
After defining the entry point to the application, the next step is to define the FLASK_CBLUEPRINTS_DIRECTORY variable, which is crucial for the extension to know where to create the blueprints you will be using. By default, this is set to 'app/blueprint', but you are free to change the path.

```python
import flask

app = flask.Flask(__name__)
app.FLASK_CBLUEPRINTS_DIRECTORY = 'you blueprint directory' 
```

After configuring the directory where blueprints will be generated, we need to instantiate the extension.

```python
from flask_cblueprint import FlaskCBlueprint

flask_cblueprint = FlaskCBlueprint()
flask_cblueprint.init_app(app)
```

Once the extension is instantiated and configured, a series of commands will be added to the Flask CLI.

```bash
$ flask app
```
```bash
Usage: flask app [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create-blueprint  > It creates a blueprint folder structure, creates a...
  list-blueprints   It lists all the available blueprints in the...

```

To create a blueprint, you can execute the following command
```bash 
$ flask app create-blueprint
```

After executing the command, follow the instructions to create the blueprint.

```bash
Enter you app name [app]: 
Enter blueprint name: test_blueprint
Create default model? [Y/n]: y
Set your initial url rule [/]: /test_blueprint
Skeleton: default
View style: Standard (url rule decorator)
[x] Structure created.
[x] Model created
[x] View style updated according to Standard (url rule decorator)
[x] Template variables injected.
All done. Now you can start customizing your newly created blueprint.
```

Once you have generated your new blueprint, you need to register it in your Flask application so that it can be accessed.

```python
def register_blueprints(app):
    ...
```