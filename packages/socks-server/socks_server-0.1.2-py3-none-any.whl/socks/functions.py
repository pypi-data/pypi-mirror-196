import os
import re

from .exeptions import *
from .constants import *
from .classes import *
from .utils import *


def renderTemplate(template, **kwargs):
    """
    Render a template with the given arguments.
    """
    try:
        with open(os.path.join(getAppRunDir(), "templates", template), "r") as f:
            template = f.read()
    except FileNotFoundError:
        raise TemplateNotFoundException(template)

    # Replace all template variables with the given arguments. If a variable is not found, it is left as is.
    # We use a regular expression to find all template variables.
    for key, value in kwargs.items():
        template = re.sub(r"{{ " + key + " }}", value, template)

    return Response(template, contentType="text/html")
