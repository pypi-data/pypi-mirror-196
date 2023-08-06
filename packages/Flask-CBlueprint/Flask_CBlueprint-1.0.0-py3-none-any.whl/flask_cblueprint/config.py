from dotenv import load_dotenv
load_dotenv()

# FLASK_CBLUEPRINTS_DIRECTORY = os.getenv('FLASK_BLUEPRINT_FOLDER', 'app/blueprints')
BLUEPRINTS_BOILERPLATE = "flask_cblueprint/__boilerplate__"
BLUEPRINTS_VIEW_STYLES = [
    ["None", ""],
    ["Standard (url rule decorator)", BLUEPRINTS_BOILERPLATE + "/views/standard"],
    ["flask.views.View", BLUEPRINTS_BOILERPLATE + "/views/flask_view"],
    ["flask.views.MethodView", BLUEPRINTS_BOILERPLATE + "/views/flask_mv"]
]

FLASK_LINK_VIEWS = 'https://flask.palletsprojects.com/en/2.2.x/views/'