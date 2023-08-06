import dash_leaflet as dl
from dash import dcc, html
import dash_bootstrap_components as dbc
import visdcc

from .api import api_model_options
from .styling import (
    button_style,
    SIDEBAR_STYLE,
    center_align,
    sidebar_input_style,
    sidebar_row_button_style,
)


### Layout styling and content ###

map_div = html.Div(
    children=[
        dl.Map(
            id="map",
            zoom=2,
            children=[
                dl.TileLayer(),
                dl.FeatureGroup(
                    [
                        dl.EditControl(
                            id="edit_control",
                            draw=dict(circle=False, circlemarker=False, polyline=False),
                        ),
                    ]
                ),
            ],
            style={
                "width": "90%",
                "height": "75vh",
                "margin": "2rem",
                "padding": "1rem",
                "border": "2px solid black",
            },
        ),
        html.Div(
            id="geojson",
        ),
    ],
    id="map-div",
    style={
        "display": "flex",
        "justifyContent": "center",
        "padding": "auto",
        "alignItems": "center",
    },
)

plain_ini_editor_div = html.Div(
    children=[
        html.H3(
            "ini file",
            style={
                "display": "block",
                "margin": "0.5rem",
                "textAlign": "center",
            },
        ),
        dbc.Textarea(
            id="ini-file-text-area",
            style={
                "width": "90%",
                "height": "75vh",
                "margin": "auto",
                "padding": "1rem",
            },
            contenteditable=False,
            readOnly=True,
        ),
    ],
)


component_editor_div = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H3(
                        "Model components",
                        id="model-components-header",
                        style={
                            "textAlign": "center",
                            "margin": "0.5rem",
                        },
                    ),
                )
            ],
            style={
                "width": "90%",
                "margin": "auto",
                "padding": "auto",
                "horizontalAlign": "middle",
            },
        ),
        dbc.Row(
            [
                dcc.Dropdown(
                    id="model-component-dropdown",
                    placeholder="Select a model setup or write method",
                    options={},
                    multi=False,
                )
            ],
            style={
                "width": "80%",
                "margin": "auto",
                "padding": "10px",
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                            "Validate",
                            id="validate-components",
                            color="primary",
                            className="mb-3",
                            n_clicks=0,
                            style=button_style(**{"width": "100%"}),
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Reset",
                            id="reset-components",
                            color="primary",
                            className="mb-3",
                            n_clicks=0,
                            style=button_style(**{"width": "100%"}),
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Remove",
                            id="del-active-component",
                            color="primary",
                            className="mb-3",
                            n_clicks=0,
                            style=button_style(**{"width": "100%"}),
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Move up",
                            id="move-up-active-component",
                            color="primary",
                            className="mb-3",
                            n_clicks=0,
                            style=button_style(**{"width": "100%"}),
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Move down",
                            id="move-down-active-component",
                            color="primary",
                            className="mb-3",
                            n_clicks=0,
                            style=button_style(**{"width": "100%"}),
                        ),
                    ]
                ),
            ],
            style={
                "width": "90%",
                "margin": "auto",
                "padding": "10px",
            },
        ),
        dbc.Row(
            [
                dbc.Accordion(id="component-input-form"),
            ],
            style={
                "width": "90%",
                "margin": "auto",
                "padding": "auto",
                "overflowY": "auto",
                "height": "60vh",
            },
        ),
    ],
    id="model-component-page",
)


model_log_div = html.Div(
    children=[
        html.H3(
            "Model log",
            style={
                "display": "block",
                "margin": "0.5rem",
                "textAlign": "center",
            },
        ),
        dbc.Textarea(
            id="log-text-area",
            readOnly=True,
            style={
                "width": "90%",
                "height": "75vh",
                "margin": "auto",
                "padding": "1rem",
                # "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgb(0 0 0 / 19%)",
            },
        ),
        dcc.Interval(id="log-interval", disabled=True),
    ],
    style={"height": "100%"},
)


tabs = html.Div(
    [
        html.Div(
            map_div, id="map-div-tab", style={"width": "100%", "alignItems": "center"}
        ),
        html.Div(
            plain_ini_editor_div,
            id="plain-ini-editor-div-tab",
            style={
                "display": "none",
                "width": "100%",
            },
        ),
        html.Div(
            component_editor_div,
            id="component-editor-div-tab",
            style={
                "display": "none",
                "width": "100%",
                "verticalAlign": "top",
            },  # "alignItems": "top", "justifyContent": "center"},
        ),
        html.Div(
            model_log_div,
            id="model-log-div-tab",
            style={"display": "none", "width": "100%"},
        ),
    ],
    style=SIDEBAR_STYLE(**{"alignItems": "top", "margin": "auto", "padding": "auto"}),
)

help_offcanvas = dbc.Offcanvas(
    [dbc.Textarea(id="help-text", readOnly=True, style={"height": "85vh"})],
    id="help-offcanvas",
    scrollable=True,
    title="Help",
    backdrop=False,
    placement="end",
    is_open=False,
)

nav_bar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.NavbarBrand("HydroMT Dashboard", style={"paddingLeft": "1rem"}),
                    width=4,
                ),
                dbc.Col(
                    dbc.Button(
                        "Help",
                        id="help-button",
                        style={
                            "float": "right",
                            "backgroundColor": "#080C80",
                            "borderColor": "white",
                            "color": "white",
                        },
                        outline=True,
                        className="me-1",
                    ),
                    width=4,
                ),
            ],
            justify="between",
            style={"width": "100%"},
        ),
    ],
    color="#080C80",
    # fluid=True,
    # links_left=True,
    dark=True,
    expand="lg",
    style={
        "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgb(0 0 0 / 19%)",
        "padding": "1rem",
        "width": "100%",
        "maxWidth": "100%",
    },
)


sidebar_model_tab = html.Div(
    [
        html.H4("Model", style=sidebar_input_style()),
        html.Hr(),
        dcc.Dropdown(
            options=api_model_options(),
            id="model-dropdown",
            placeholder="plugin",
            style=sidebar_input_style(),
        ),
        dbc.Label("Model root"),
        dbc.Input(
            id="model-output-path",
            type="text",
            style=sidebar_input_style(),
        ),
        html.Div(
            dbc.Button(
                "Select folder",
                id="output-path-button",
                style=button_style(**sidebar_input_style()),
            ),
            style=sidebar_row_button_style(),
        ),
    ],
    style={"backgroundColor": "#Ffffff", "height": "100%", "padding": "1rem"},
)

sidebar_data_tab = dbc.Container(
    [
        html.H4("Data Catalog", style=sidebar_input_style()),
        html.Hr(),
        dcc.Dropdown(
            options=[
                {"label": "Deltares data catalog", "value": "deltares_data"},
                {"label": "Other data catalog", "value": "other data catalog"},
            ],
            multi=True,
            searchable=True,
            value="deltares_data",
            id="data-catalog-options",
            style=sidebar_input_style(),
        ),
        dcc.Upload(
            dbc.Button("Upload file", style=button_style(**sidebar_input_style())),
            id="upload-data-catalog",
            accept=".yml, .yaml",
            style=sidebar_row_button_style(),
        ),
    ],
    style={"backgroundColor": "#Ffffff", "height": "100%", "padding": "1rem"},
)
sidebar_region_tab = html.Div(
    [
        html.H4("Region", style=sidebar_input_style()),
        html.Hr(),
        dcc.Dropdown(
            options=[
                {"label": "Geometry", "value": "geom"},
                {"label": "Bounding box", "value": "bbox"},
                {"label": "Basin", "value": "basin"},
                {"label": "Subbasin", "value": "subbasin"},
                {"label": "Interbasin", "value": "interbasin"},
            ],
            id="region-options",
            style=sidebar_input_style(),
        ),
        html.Div(
            [
                dbc.Label("Variable-Threshold pairs"),
                html.Div(
                    children=[],
                    id="variable-threshold-inputs",
                ),
                dbc.Button(
                    "+",
                    id="variable-threshold-btn",
                    style=button_style(**center_align()),
                ),
            ],
            id="variable-threshold-div",
            style={"display": "none"},
        ),
        html.P(
            "Draw a region on the map",
            style={"font-style": "italic"},
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Button(
                    "Preview region",
                    id="region-preview-button",
                    disabled=True,
                    style=button_style(
                        **{
                            "display": "flex",
                            "justifyContent": "center",
                            "textAlign": "center",
                            "margin": "auto",
                            "width": "100%",
                        }
                    ),
                )
            ],
            align="center",
            style=sidebar_row_button_style(),
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Button(
                    "Clear map",
                    id="clear-map-button",
                    style=button_style(
                        **{
                            "display": "flex",
                            "justifyContent": "center",
                            "textAlign": "center",
                            "margin": "auto",
                            "width": "100%",
                        }
                    ),
                )
            ],
            align="center",
            style=sidebar_row_button_style(),
        ),
    ],
    style={"backgroundColor": "#Ffffff", "height": "100%", "padding": "1rem"},
)
sidebar_config_tab = html.Div(
    [
        html.H4("Configuration", style=sidebar_input_style()),
        html.Hr(),
        html.Div(
            [
                dcc.Upload(
                    dbc.Button("Upload", id="upload-ini-button", style=button_style()),
                    id="upload-ini",
                    accept=".ini",
                    disable_click=False,
                    style=sidebar_row_button_style(),
                ),
                html.Br(),
                dcc.Dropdown(
                    options=[
                        {"label": "Delft-FIAT", "value": "fiat"},
                        {"label": "DELWAQ", "value": "delwaq"},
                        {"label": "SFINCS", "value": "sfincs"},
                        {"label": "Wflow", "value": "wflow"},
                    ],
                    placeholder="Template",
                    id="template-dropdown",
                    style=sidebar_input_style(),
                ),
                html.Div(
                    [
                        dbc.Alert(
                            "Please select a model plugin first",
                            duration=3000,
                            color="danger",
                            style={"margin": "0.5rem 0rem"},
                            is_open=False,
                            id="config-alert",
                            fade=True,
                        )
                    ],
                    id="config-alert-div",
                    style=sidebar_input_style(),
                ),
                html.Hr(),
                dbc.Row(
                    dbc.Button(
                        ".ini editor",
                        id="ini-editor-button",
                        style=button_style(
                            **{
                                "margin": "auto",
                            }
                        ),
                    ),
                    style=sidebar_row_button_style(),
                ),
                html.Br(),
                dbc.Row(
                    dbc.Button(
                        "Component editor",
                        id="component-editor-button",
                        style=button_style(
                            **{
                                "display": "flex",
                                "justifyContent": "center",
                                "textAlign": "center",
                                "margin": "auto",
                            }
                        ),
                    ),
                    style=sidebar_row_button_style(),
                ),
            ]
        ),
    ],
    style={
        "backgroundColor": "#Ffffff",
        "height": "100%",
        "padding": "1rem",
        "width": "100%",
        "marginRight": "0.5rem",
    },
)

build_model_tab = html.Div(
    [
        html.H4("Build model", style=sidebar_input_style()),
        html.Hr(),
        html.Div(
            [
                dcc.Loading(
                    id="build-model-loading",
                    type="circle",
                    children=[
                        html.Div(
                            dbc.Button(
                                ["Build model"],
                                id="model-build-button",
                                n_clicks=0,
                                style=button_style(),
                            ),
                            style=sidebar_row_button_style(),
                        )
                    ],
                ),
                visdcc.Run_js(id="javascriptLog", run=""),
            ],
            id="build-model-div",
        ),
        html.Br(),
        dbc.Alert(
            "The given model data/parameters are incomplete",
            id="model-build-alert",
            color="danger",
            is_open=False,
        ),
    ],
    style={
        "backgroundColor": "#Ffffff",
        "height": "100%",
        "padding": "1rem",
        "width": "100%",
        "marginRight": "0.5rem",
    },
)

sidebar_tabs = dbc.Container(
    [
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Model",
                    value="Model",
                    children=[sidebar_model_tab],
                    className="model-view-tab",
                    selected_className="model-view-tab-active",
                ),
                dcc.Tab(
                    label="Data",
                    value="Data",
                    children=[sidebar_data_tab],
                    className="model-view-tab",
                    selected_className="model-view-tab-active",
                ),
                dcc.Tab(
                    label="Region",
                    value="Region",
                    children=[sidebar_region_tab],
                    className="model-view-tab",
                    selected_className="model-view-tab-active",
                ),
                dcc.Tab(
                    label="Config",
                    value="Config",
                    children=[sidebar_config_tab],
                    className="model-view-tab",
                    selected_className="model-view-tab-active",
                ),
                dcc.Tab(
                    label="Build",
                    value="Build",
                    children=[build_model_tab],
                    className="model-view-tab",
                    selected_className="model-view-tab-active",
                ),
            ],
            className="model-view-tab-container",
            content_style={"justify": "center"},
            vertical=True,
            colors={"primary": "#ffffff"},
            id="sidebar-tabs",
            value="Model",
        ),
    ],
    style=SIDEBAR_STYLE(**{"alignItems": "top", "margin": "auto", "padding": "1rem"}),
)

page_content = html.Div(
    [
        dcc.Store(id="model-input-data"),
        dcc.Store(id="geojson-data"),
        dcc.Store(id="component-data"),
        dbc.Container(
            [
                dbc.Row(nav_bar),
                dbc.Row(
                    [
                        dbc.Col(
                            sidebar_tabs,
                            width=3,
                            style={
                                "min-width": "20rem",
                                "padding": "1rem",
                                "height": "100%",
                            },
                        ),
                        dbc.Col(
                            tabs,
                            width=9,
                            style={
                                "padding": "1rem",
                                "height": "100%",
                            },
                            align="center",
                        ),
                    ],
                ),
            ],
            fluid=True,
            style={
                "height": "100%",
                "width": "100%",
                "backgroundColor": "#ccc",
                "justifyContent": "center",
            },
        ),
        help_offcanvas,
    ],
    style={"height": "100vh"},
)
