from fastapi import Request
from fastapi.templating import Jinja2Templates
import os
import sys

# Determine the directory where the Jinja2 templates are stored.
# If the application is frozen (e.g., packaged with PyInstaller), the templates directory is located within the temporary directory (_MEIPASS).
# Otherwise, the templates directory is located relative to the current file's directory.

if getattr(sys, 'frozen', False):
    templates_dir = os.path.join(sys._MEIPASS, 'templates')
else:
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

# Initialize Jinja2Templates with the determined templates directory
templates = Jinja2Templates(directory=templates_dir)

def render_index(request: Request, division_options, area_options, doc_options, generated_code=None):
    """
    Renders the 'index.html' template with the provided options and generated code.

    Parameters:
    -----------
    request : Request
        The FastAPI request object, which provides context about the HTTP request.
    division_options : list
        A list of options to populate the division dropdown in the HTML form.
    area_options : list
        A list of options to populate the area dropdown in the HTML form.
    doc_options : list
        A list of options to populate the document dropdown in the HTML form.
    generated_code : str, optional
        The generated code to be displayed in the HTML template. Default is None.

    Returns:
    --------
    TemplateResponse
        A Jinja2 template response that renders the 'index.html' template with the provided context.
    """

    return templates.TemplateResponse("index.html", {
        "request": request,  # Passes the request context to the template.
        "division_options": division_options,  # Populates division dropdown in the template.
        "area_options": area_options,  # Populates area dropdown in the template.
        "doc_options": doc_options,  # Populates document dropdown in the template.
        "generated_code": generated_code  # Displays the generated code in the template if provided.
    })
