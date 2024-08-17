from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import threading
import webbrowser
import uvicorn
import os
import sys
from models import CodeManager
from views import render_index

# Create a FastAPI application instance.
app = FastAPI()

# Determine the directory where the static files (e.g., CSS, images) are stored.
# If the application is frozen (e.g., packaged with PyInstaller), the static directory is located within the temporary directory (_MEIPASS).
# Otherwise, the static directory is located relative to the current file's directory.

if getattr(sys, 'frozen', False):
    static_dir = os.path.join(sys._MEIPASS, 'static')
else:
    static_dir = os.path.join(os.path.dirname(__file__), 'static')

# Mount the static files directory so that they can be accessed via the "/static" path in the application.
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize an instance of the CodeManager class, which is responsible for generating and managing codes.
code_manager = CodeManager()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Handle GET requests to the root URL ("/").
    This route renders the index page with dropdown options for division, area, and document codes.

    Parameters:
    -----------
    request : Request
        The FastAPI request object, which provides context about the HTTP request.

    Returns:
    --------
    HTMLResponse
        A Jinja2 template response that renders the 'index.html' template with the provided dropdown options.
    """
    # Define the options for the dropdown menus.
    division_options = ['XGM', 'XGA', 'BBM', 'BBB', 'BRB', 'BLP', 'BLX', 'TRV']
    area_options = ['XDM', 'XOG', 'YPE', 'TRV', 'QLE', 'XDM', 'TIS', 'D&P', 'NEG', 'MRS', 'TNI', 'KOM']
    doc_options = ['XRO', 'XRC', 'FAR', 'TNS', 'XAN', 'YOL']

    # Render the index page with the options.
    return render_index(request, division_options, area_options, doc_options)

@app.post("/generate_code/", response_class=HTMLResponse)
async def generate_code(request: Request, division_code: str = Form(...), area_code: str = Form(...), doc_code: str = Form(...)):
    """
    Handle POST requests to the "/generate_code/" URL.
    This route generates a new code based on the provided division, area, and document codes, and then renders the index page with the generated code.

    Parameters:
    -----------
    request : Request
        The FastAPI request object, which provides context about the HTTP request.
    division_code : str
        The division code selected by the user in the form.
    area_code : str
        The area code selected by the user in the form.
    doc_code : str
        The document code selected by the user in the form.

    Returns:
    --------
    HTMLResponse
        A Jinja2 template response that renders the 'index.html' template with the provided dropdown options and the newly generated code.
    """
    # Generate a new code using the CodeManager instance.
    full_code = code_manager.generate_code(division_code, area_code, doc_code)

    # Reuse the same options for the dropdown menus.
    division_options = ['XGM', 'XGA', 'BBM', 'BBB', 'BRB', 'BLP', 'BLX', 'TRV']
    area_options = ['XDM', 'XOG', 'YPE', 'TRV', 'QLE', 'XDM', 'TIS', 'D&P', 'NEG', 'MRS', 'TNI', 'KOM']
    doc_options = ['XRO', 'XRC', 'FAR', 'TNS', 'XAN', 'YOL']

    # Render the index page with the options and the generated code.
    return render_index(request, division_options, area_options, doc_options, generated_code=full_code)

def open_browser():
    """
    Opens the default web browser to the application's URL.
    This function is called in a separate thread to ensure the browser opens automatically when the server starts.
    """
    webbrowser.open_new("http://127.0.0.1:8000")

if __name__ == "__main__":
    # Start a timer that will open the web browser after 1.25 seconds.
    threading.Timer(1.25, open_browser).start()

    # Run the FastAPI application using Uvicorn, a lightning-fast ASGI server.
    uvicorn.run(app, host="127.0.0.1", port=8000)