import re
import click


def validate_name(ctx, param, value):
    """
    It checks if the value passed to the `--name` option is a valid blueprint name
    
    :param ctx: The context object
    :param param: The name of the parameter
    :param value: The value of the parameter
    :return: The value of the parameter.
    """
    def fail(text):
        ctx.fail(click.style(text, fg="red", bold=True))

    if not bool(re.match("^[a-z0-9_]*$", value)):
        fail("Blueprint name must contain lowercase characters and/or underscore symbol.")

    if not bool(re.match("^[a-z]*$", value[0])):
        fail("Blueprint name must start with a letter.")

    return value