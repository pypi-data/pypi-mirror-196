import webbrowser
from threading import Timer

from .app import app


def main():

    host = "localhost"
    port = 8080
    folder = "hydromt-dash"
    url = f"http://{host}:{port}/{folder}/"
    Timer(10, webbrowser.open_new(url))

    # run app
    app.run(
        host=host,
        port=port,
    )


def dev():
    app.run(debug=True)
