"""HydroMT Dashboard application"""
from dash import dcc, html, Dash
import dash_bootstrap_components as dbc
import logging
import io
from .layouts import page_content
from .callbacks import *

url_bar_and_content_div = html.Div([page_content])

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
    ],
    suppress_callback_exceptions=True,
)
app.config.suppress_callback_exceptions = True
app.layout = url_bar_and_content_div
app.title = "HydroMT Dashboard"
