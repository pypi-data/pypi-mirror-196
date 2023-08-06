from setuptools import setup

# Opening the README.md file and assigning it to the variable `readme`.
readme = open("./README.md", "r")

# A setup function that is used to install the package.
setup(
    name="Flask-CBlueprint",
    install_requires=[
        "Flask>=1.0.4",
        "Werkzeug>=1.0.1",
        "click>=8.1.3",
        "MarkupSafe>=2.1.2",
        "python-dotenv>=1.0.0",
        "simple-term-menu>=1.6.1",
    ],
)