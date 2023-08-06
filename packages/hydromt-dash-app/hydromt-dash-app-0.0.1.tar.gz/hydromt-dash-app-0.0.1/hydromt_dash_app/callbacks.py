from typing import Union, Tuple
import os
import logging
import io

from dash import Output, Input, State, callback, ALL, callback_context
import dash_leaflet as dl
from dash.exceptions import PreventUpdate

from .functions import (
    model_component_inputs,
    decode_file,
    input_to_dict,
    validate_inputs,
    ini_to_dict,
    dict_to_ini,
    save_geojson,
    create_variable_threshold_pairs,
    get_folder,
    get_output_dir,
    parse_mapdata,
    build_model,
)
from .api import api_model_components, api_datasets, get_component_docs, api_get_region

logger = logging.getLogger()
log_capture_string = io.StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


### General callbacks ###


@callback(
    Output("map-div-tab", "style"),
    Output("plain-ini-editor-div-tab", "style"),
    Output("component-editor-div-tab", "style"),
    Output("model-log-div-tab", "style"),
    Input("sidebar-tabs", "value"),
    Input("component-editor-button", "n_clicks"),
    Input("ini-editor-button", "n_clicks"),
    State("map-div-tab", "style"),
    State("plain-ini-editor-div-tab", "style"),
    State("component-editor-div-tab", "style"),
    State("model-log-div-tab", "style"),
)
def change_content_tabs(
    active_tab,
    component_editor_button,
    ini_editor_button,
    map_div_style,
    plain_ini_div_style,
    component_editor_div_style,
    model_log_div_style,
):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "component-editor-button" in changed_id:
        plain_ini_div_style.update({"display": "none"})
        component_editor_div_style.update({"display": "inline-block"})
        model_log_div_style.update({"display": "none"})
        map_div_style.update({"display": "none"})

    elif "ini-editor-button" in changed_id:
        plain_ini_div_style.update({"display": "inline-block"})
        component_editor_div_style.update({"display": "none"})
        model_log_div_style.update({"display": "none"})
        map_div_style.update({"display": "none"})

    elif active_tab in ["Model", "Data", "Region"]:
        map_div_style.update({"display": "inline-block"})
        plain_ini_div_style.update({"display": "none"})
        component_editor_div_style.update({"display": "none"})
        model_log_div_style.update({"display": "none"})

    elif active_tab == "Config":
        plain_ini_div_style.update({"display": "inline-block"})
        component_editor_div_style.update({"display": "none"})
        model_log_div_style.update({"display": "none"})
        map_div_style.update({"display": "none"})

    elif active_tab == "Build":
        plain_ini_div_style.update({"display": "none"})
        component_editor_div_style.update({"display": "none"})
        model_log_div_style.update({"display": "inline-block"})
        map_div_style.update({"display": "none"})

    else:
        raise PreventUpdate

    return (
        map_div_style,
        plain_ini_div_style,
        component_editor_div_style,
        model_log_div_style,
    )


@callback(
    Output("help-offcanvas", "is_open"),
    Output("help-text", "value"),
    Input("help-button", "n_clicks"),
    State("help-offcanvas", "is_open"),
    Input("component-input-form", "active_item"),
    State("model-dropdown", "value"),
    prevent_initial_call=True,
)
def toggle_help_window(n1: int, is_open: bool, active_component, model_name) -> bool:
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]

    if "help-button" in changed_id or is_open:
        if active_component:
            docs = get_component_docs(model_name, active_component)
            return True, docs
        else:
            return True, "Please select an active component"
    return is_open, []


@callback(
    Output("model-input-data", "data"),
    Input("model-dropdown", "value"),
)
def store_components_data(model):
    if model:
        return api_model_components(model)
    raise PreventUpdate()


@callback(
    Output("edit_control", "draw"),
    Input("region-options", "value"),
)
def update_mapdraw_tools(region_option: str) -> dict:
    if region_option == "geom":
        return dict(
            circle=False,
            circlemarker=False,
            polyline=False,
            marker=False,
            rectangle=False,
        )
    if region_option == "bbox":
        return dict(
            circle=False,
            circlemarker=False,
            polyline=False,
            marker=False,
            polygon=False,
        )
    if region_option in ["basin", "subbasin"]:
        return dict(circle=False, circlemarker=False, polyline=False)
    if region_option == "interbasin":
        return dict(circle=False, circlemarker=False, polyline=False, marker=False)
    else:
        return dict(
            circle=False,
            circlemarker=False,
            polyline=False,
            marker=False,
            polygon=False,
            rectangle=False,
        )


### sidebar callbacks ###
@callback(Output("model-output-path", "value"), Input("output-path-button", "n_clicks"))
def get_output_path(n_clicks: int) -> str:
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "output-path-button" in changed_id:
        path = get_folder()
        return path if path else ""
    else:
        return get_output_dir()


@callback(
    Output("geojson-data", "data"),
    Input("edit_control", "geojson"),
    State("model-output-path", "value"),
)
def parse_geojson(map_data: dict, model_root: str) -> dict:
    if map_data:
        if map_data["features"]:
            if map_data["features"][0]["properties"]["type"] == "polygon":
                save_geojson(map_data["features"][0], model_root)
            return map_data


@callback(
    Output("region-preview-button", "disabled"),
    Output("clear-map-button", "disabled"),
    Input("edit_control", "geojson"),
)
def enable_preview_button(map_data):
    if map_data:
        if map_data["features"]:
            return False, False
        else:
            return True, True
    else:
        raise PreventUpdate()


@callback(
    Output("map", "children"),
    Input("region-preview-button", "n_clicks"),
    Input("clear-map-button", "n_clicks"),
    State("geojson-data", "data"),
    State("region-options", "value"),
    State("model-output-path", "value"),
    State("data-catalog-options", "value"),
    State("map", "children"),
    State({"type": "variable", "index": ALL}, "value"),
    State({"type": "threshold", "index": ALL}, "value"),
)
def preview_region(
    preview_click,
    clear_map_click,
    map_data,
    region_option,
    model_root,
    data_libs,
    map_children,
    variables,
    thresholds,
):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "region-preview-button" in changed_id:
        if map_data:

            if variables and thresholds:
                region_dict = parse_mapdata(
                    map_data, model_root, region_option, variables, thresholds
                )
            else:
                region_dict = parse_mapdata(map_data, model_root, region_option)

            region_geojson = api_get_region(region_dict, data_libs)
            map_children.append(dl.GeoJSON(data=region_geojson))
            return map_children
        else:
            raise PreventUpdate()
    elif "clear-map-button" in changed_id:
        if map_data:
            return [
                dl.TileLayer(),
                dl.FeatureGroup(
                    [
                        dl.EditControl(
                            id="edit_control",
                            draw=dict(circle=False, circlemarker=False, polyline=False),
                        ),
                    ]
                ),
            ]
        else:
            raise PreventUpdate()
    else:
        raise PreventUpdate()


@callback(
    Output("variable-threshold-inputs", "children"),
    Input("variable-threshold-btn", "n_clicks"),
    State("variable-threshold-inputs", "children"),
    Input("region-options", "value"),
)
def add_variable_threshold_pairs(
    n_clicks: int, children: list, region_option: str
) -> list:
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if not n_clicks:
        n_clicks = 1
    if "region-options" in changed_id and region_option == "subbasin":
        children.append(
            create_variable_threshold_pairs(index=n_clicks, var="strord", thresh="3")
        )
        return children
    elif "variable-threshold-btn" in changed_id:
        children = children if children else []

        children.append(create_variable_threshold_pairs(index=n_clicks))
        return children
    else:
        raise PreventUpdate


@callback(Output("variable-threshold-div", "style"), Input("region-options", "value"))
def toggle_variable_threshold(region_option: str) -> dict:
    if region_option in ["basin", "subbasin", "interbasin"]:
        return {"display": "block"}
    else:
        return {"display": "none"}


@callback(
    Output("data-catalog-options", "value"),
    Output("data-catalog-options", "options"),
    Input("upload-data-catalog", "filename"),
    State("data-catalog-options", "value"),
    State("data-catalog-options", "options"),
)
def show_data_catalog_in_dropdown(
    filename: str, dropdown_values: Union[str, list], dropdown_options: list
) -> Tuple[Union[str, list], list]:
    if filename:

        filename_option = {"label": filename, "value": filename}
        if dropdown_values:

            if isinstance(dropdown_values, str):
                dropdown_values = [dropdown_values]
            dropdown_values.append(filename)
            dropdown_options.append(filename_option)

            return dropdown_values, dropdown_options
        else:
            dropdown_options.append(filename_option)
            return filename, dropdown_options
    else:
        raise PreventUpdate


@callback(
    Output("config-alert", "is_open"),
    Output("upload-ini", "disable_click"),
    Input("upload-ini-button", "n_clicks"),
    Input("model-dropdown", "value"),
)
def config_upload_alert(n_clicks: int, model_dropdown_value: str):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if model_dropdown_value:
        return False, False

    elif "upload-ini-button" in changed_id and not model_dropdown_value:
        return True, True

    else:
        return False, True


@callback(
    Output("build-model-loading", "children"),
    Output("model-build-alert", "is_open"),
    Input("model-build-button", "n_clicks"),
    State("model-output-path", "value"),
    State("model-dropdown", "value"),
    State("data-catalog-options", "value"),
    State("ini-file-text-area", "value"),
    State("geojson-data", "data"),
    State("region-options", "value"),
    State("build-model-loading", "children"),
    State({"type": "variable", "index": ALL}, "value"),
    State({"type": "threshold", "index": ALL}, "value"),
)
def model_build_callback(
    build_button: int,
    model_root: str,
    model_plugin: str,
    data_libs: str,
    ini_file: str,
    map_data: dict,
    region_option: str,
    loading_children: dict,
    variables: list,
    thresholds: list,
):
    changed_id = callback_context.triggered[0]["prop_id"].split(".")[0]
    if "model-build-button" in changed_id:
        if all(
            [
                model_root,
                model_plugin,
                data_libs,
                ini_file,
                map_data,
                region_option,
            ]
        ):

            model_name = os.path.basename(model_root)
            ini_path = os.path.join(model_root, f"{model_name}.ini")
            with open(ini_path, "w") as file:
                file.write(ini_file)

            if variables and thresholds:

                region = parse_mapdata(
                    map_data, model_root, region_option, variables, thresholds
                )
            else:
                region = parse_mapdata(map_data, model_root, region_option)

            if isinstance(data_libs, str):
                data_libs = [data_libs]

            build_model(model_plugin, model_root, region, ini_path, data_libs)

            return loading_children, False

        else:
            return loading_children, True

    else:
        raise PreventUpdate


@callback(
    Output("log-text-area", "value"),
    Output("log-interval", "disabled"),
    Output("javascriptLog", "run"),
    Input("log-interval", "n_intervals"),
    Input("model-build-button", "n_clicks"),
    State("build-model-loading", "loading_state"),
    State("log-text-area", "value"),
    State("ini-file-text-area", "value"),
    State("model-dropdown", "value"),
)
def stream_log(n, build_button, loading_state, log_field, ini_field, model_plugin):

    if build_button and ini_field and model_plugin:
        if log_field:
            if "Model build finished" in log_field:
                return log_field, True, ""
        log_contents = log_capture_string.getvalue()
        if loading_state:
            if not loading_state["is_loading"]:
                return log_field, True, ""
        logCMD = """
        var textarea = document.getElementById('log-text-area');
        textarea.scrollTop = textarea.scrollHeight;       
        """

        return log_contents, False, logCMD
    else:
        raise PreventUpdate


### Component editor callbacks ###
@callback(
    Output("model-components-header", "children"),
    Input("model-dropdown", "value"),
    Input("sidebar-tabs", "value"),
)
def update_component_header(model_plugin_value: str, tab: str) -> str:
    if tab == "Config":
        if model_plugin_value:

            return f"{model_plugin_value.capitalize()} model components"
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@callback(
    Output("model-component-dropdown", "options"),
    Input("model-dropdown", "value"),
    Input("sidebar-tabs", "value"),
    Input("component-input-form", "children"),
    # prevent_initial_call=True
)
def update_components_dropdown(
    model_plugin_value: str,
    tab: str,
    children: list,
) -> list:

    options = []
    active_components = []
    if children:
        active_components = [c["props"]["item_id"] for c in children]
    if tab == "Config" and model_plugin_value:
        model_inputs = api_model_components(model_plugin_value)
        for component in model_inputs.keys():
            if not component.split("_")[0] in ["write", "setup"]:
                continue
            if component in active_components:
                i = 2
                while f"{component}{i}" in active_components:
                    i += 1
                options.append({"label": f"{component}{i}", "value": f"{component}{i}"})
            else:
                options.append({"label": component, "value": component})
    return options


@callback(
    Output("component-input-form", "children"),
    Output("component-input-form", "active_item"),
    Input("model-component-dropdown", "value"),
    Input("model-dropdown", "value"),
    Input("upload-ini", "contents"),
    State("ini-file-text-area", "value"),
    State("component-input-form", "children"),
    State("component-input-form", "active_item"),
    Input("component-editor-button", "n_clicks"),
    State("model-input-data", "data"),
    State("data-catalog-options", "value"),
    Input("reset-components", "n_clicks"),
    Input("del-active-component", "n_clicks"),
    Input("move-up-active-component", "n_clicks"),
    Input("move-down-active-component", "n_clicks"),
    Input("validate-components", "n_clicks"),
)
def render_component_inputs(
    component: str,
    model: str,
    uploaded_content: str,
    ini_txt: str,
    children: list,
    active_child: str,
    component_editor_button: int,
    model_inputs: dict,
    datacatalog: list,
    *args,
) -> Tuple[list, str]:
    if datacatalog:
        datasets = api_datasets(datacatalog)
    changed_id = callback_context.triggered[0]["prop_id"].split(".")[0]
    if changed_id == "model-component-dropdown" and component and model:

        children = children if children else []
        # TODO template / plain ini config values from store
        children.append(
            model_component_inputs(model_inputs, component, datasets, template={})
        )

    elif "upload-ini" in changed_id:
        ini_content = decode_file(uploaded_content)

        cfdict = ini_to_dict(ini_content)

        children = []
        for component in cfdict:
            print(component)
            children.append(
                model_component_inputs(
                    model_inputs, component, datasets, template=cfdict
                )
            )

    elif changed_id == "reset-components":
        children, component = [], ""
    elif changed_id == "validate-components" and children:
        children_out = []
        for child in children:
            name = child["props"]["item_id"]
            state = "success" if validate_inputs(child) else "warning"
            child["props"]["title"] = f"{name} - {state.upper()}"
            # TODO apply color to button or add icon
            # colors={'success': '#d1e7dd', 'warning': '#fff3cd'}
            # child['props']['style'].update({'background-color': colors[state]})
            children_out.append(child)
        component = ""  #  close all
        children = children_out
    elif children and active_child:
        children_names = [c["props"]["item_id"] for c in children]
        if changed_id == "del-active-component":
            i = children_names.index(active_child)
            children.pop(i)
            component = ""
            if len(children_names) > 1:
                component = children_names[i - 1 if i >= 1 else i + 1]
        elif changed_id == "move-up-active-component":
            i = children_names.index(active_child)
            if i != 0:
                c = children.pop(i)
                children = children[: i - 1] + [c] + children[i - 1 :]
            component = active_child
        elif changed_id == "move-down-active-component":
            i = children_names.index(active_child)
            c = children.pop(i)
            children = children[: i + 1] + [c] + children[i + 1 :]
            component = active_child
    else:
        raise PreventUpdate
    return children, component


@callback(
    Output("ini-file-text-area", "value"),
    Input("upload-ini", "contents"),
    Input("sidebar-tabs", "value"),
    Input("upload-ini-button", "n_clicks"),
    Input("component-input-form", "children"),
    State("ini-file-text-area", "value"),
)
def render_ini_data(
    upload_contents: str,
    ini_button: int,
    active_tab: str,
    components: list,
    ini_field: str,
) -> str:

    changed_id = callback_context.triggered[0]["prop_id"].split(".")[0]
    if "component-input-form" in changed_id:
        cfdict = {}
        if components:

            for item in components:
                section, kwargs = input_to_dict(item)
                cfdict[section] = kwargs
        return dict_to_ini(cfdict)
    elif "upload-ini" in changed_id:
        if upload_contents:
            ini_content = decode_file(upload_contents)
            return ini_content

    raise PreventUpdate


@callback(
    Output("sidebar-tabs", "value"),
    Input("upload-ini", "contents"),
    Input("model-build-button", "n_clicks"),
    State("sidebar-tabs", "value"),
)
def change_active_tab(contents: str, model_build_button, active_tab: str) -> str:

    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "model-build-button" in changed_id:
        return "Build"
    elif contents:
        return "Config"

    else:
        return active_tab
