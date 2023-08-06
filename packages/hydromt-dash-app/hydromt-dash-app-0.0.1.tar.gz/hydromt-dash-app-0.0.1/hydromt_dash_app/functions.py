from configparser import ConfigParser
from ast import literal_eval
import base64
import subprocess
import os
import tkinter
from tkinter import filedialog
from typing import Tuple
import shutil
import time

from geojson import FeatureCollection, dump
import dash_bootstrap_components as dbc
from dash import dcc

# TODO replace with API
from hydromt.config import configread
from hydromt import log
from .api import api_model_entry_points, api_model_plugins


def argument_to_form(
    method: str, argument: str, dtype: str, datasets: dict, default=None
):
    """Creates a row with dash input object for a given method and method argument

    :param method: model plugin method/component
    :type method: str
    :param argument: argument of given method
    :type argument: str
    :param dtype: expected datatype of argument
    :type dtype: str
    :param default: default value of argument, defaults to None
    :type default: str, optional
    :return: a dash bootstrap row with input object
    :rtype: dash_bootstrap_components.Row
    """
    name = f"{method}.{argument}"
    kwargs = dict(
        style={"width": "300px"},
        id=name,
        placeholder=argument,
    )
    print(kwargs)
    if dtype == "bool":
        if default:
            kwargs.update(value=str(default).capitalize())
        field = dcc.Dropdown(options=["True", "False"], **kwargs)
    elif dtype == "list":
        if default:  # parse list to string
            kwargs.update(value=", ".join(default))
        field = dcc.Input(type="text", **kwargs)
    elif dtype == "float" or dtype == "int":
        if default:
            kwargs.update(value=default)
        field = dcc.Input(type="number", **kwargs)
    elif dtype in ["RasterDatasetSource", "GeoDatasetSource", "GeoDataframeSource"]:
        if default:
            kwargs.update(value=str(default))
            kwargs.pop("placeholder")
        field = dcc.Dropdown(options=datasets[dtype], **kwargs)
    else:
        if default:
            kwargs.update(value=str(default))
        field = dcc.Input(type="text", **kwargs)

    form_row = dbc.Row(
        [dbc.Label(argument, width=2), dbc.Col(field, width=5)],
        className="mb-3",
    )

    return form_row


def dict_type_inputs(component_dict: dict, component_name: str) -> list:
    """Function for creating input fields for components that have a dictionary
    type as input. For instance, setup_config

    Args:
        component_dict (dict): dictionary with component and input arguments
    """
    children = []
    for argument, value in component_dict[component_name].items():
        name = f"{component_name}.{argument}"
        kwargs = dict(
            style={"width": "300px"},
            id=name,
            placeholder=argument,
        )
        row = dbc.Row(
            [
                dbc.Col(dbc.Label(argument, width=2)),
                dbc.Col(dcc.Input(value=value, **kwargs), width=5),
            ],
            className="mb-3",
        )
        children.append(row)
    return children


def model_component_inputs(
    model_inputs: dict, component_name: str, datasets: dict, template: dict = {}
):
    """Generate the input fields for a model method.

    :param model_name: model plugin name
    :type model_name: str
    :param component_name: name of model method/component
    :type component_name: str
    :param template: dict template, defaults to {}
    :type template: dict, optional
    :return: dash bootstrap AccordionItem object with all input objects for a given model method
    :rtype: dash_bootstrap_components.AccordionItem
    """
    method_signature = model_inputs.get(component_name.strip("0123456789"), {})
    children = []
    if method_signature:
        for (argument, type) in method_signature["required"]:
            if "dict" in argument:
                dict_children = dict_type_inputs(template, component_name)
                return dbc.AccordionItem(
                    title=component_name,
                    children=dict_children,
                    item_id=component_name,
                    style={},
                )

            default = template.get(component_name, {}).get(argument, None)
            print(template)
            children.append(
                argument_to_form(component_name, argument, type, datasets, default)
            )
        for (argument, type, default) in method_signature["optional"]:
            # overwrite default with value from template

            default = template.get(component_name, {}).get(argument, default)

            children.append(
                argument_to_form(component_name, argument, type, datasets, default)
            )
        return dbc.AccordionItem(
            title=component_name, children=children, item_id=component_name, style={}
        )
    return []


def input_to_dict(child: dict) -> Tuple[str, dict]:
    """Get section and dict object from input dict

    :param child: dict of dash children
    :type child: dict
    :return: section name and dict of options
    :rtype: Tuple[str, dict]
    """
    options = {}
    section = child["props"]["item_id"]
    for item in child["props"]["children"]:
        _, input = item["props"]["children"]
        props = input["props"]["children"]["props"]
        section, argument = props["id"].split(".")[:2]
        value = props.get("value", None)
        options.update({argument: value})
    return section, options


def validate_inputs(child: dict) -> bool:
    # TODO proper check on dtypes
    return all([v is not None for v in input_to_dict(child)[1].values()])


def decode_file(contents: str) -> str:
    """Decodes base64 string to utf-8.

    :param contents: string encoded in base64
    :type contents: str
    :return: decoded string in utf-8
    :rtype: str
    """
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    return decoded.decode("utf-8")


def ini_to_dict(ini_txt: str) -> dict:
    """read model configuration from file and parse to dict.
    .
        :param ini_txt: text string from ini file
        :type ini_txt: str
        :return: dict of parsed ini file
        :rtype: dict
    """
    cf = ConfigParser(allow_no_value=True, inline_comment_prefixes=[";", "#"])
    cf.optionxform = str  # preserve capital letter
    cf.read_string(ini_txt)
    cfdict = dict()
    for section in cf.sections():
        if section not in cfdict:
            cfdict[section] = dict()  # init
        sdict = dict()
        for key, value in cf.items(section):
            try:
                v = literal_eval(value)
                assert not isinstance(v, tuple)  #  prevent tuples from being parsed
                value = v
            except Exception:
                pass
            sdict[key] = value
        cfdict[section].update(**sdict)
    return cfdict


def dict_to_ini(cfdict: dict) -> str:
    """Write model configuration to file

    :param cfdict: _description_
    :type cfdict: dict
    :return: _description_
    :rtype: str
    """
    ini_text = ""
    for component in cfdict.keys():
        ini_text += f"\n[{component}]\n"
        for arg, val in cfdict[component].items():
            ini_text += f"{arg} = {val}\n"
    return ini_text


def save_geojson(feature: dict, model_root: str = None):
    """Saves a dict in geojson format to geojson file.

    :param feature: The feature/geometry to save as a geojson file
    :type feature: dict
    :param model_root: path to model root, defaults to None
    :type model_root: str, optional
    """
    if os.path.isdir(model_root):
        file_path = os.path.join(model_root, "geom.geojson")
    else:
        file_path = "./data/geom.geojson"

    features = []
    features.append(feature)
    feature_collection = FeatureCollection(features)
    with open(file_path, "w") as f:
        dump(feature_collection, f)


def build_model(
    model: str,
    model_root: str,
    region: str,
    ini_config: str,
    data_libs: list = [],
    cli=False,
):
    """Function to build a HydroMT model.

    :param model: name of model plugin
    :type model: str
    :param model_root: path to model root
    :type model_root: str
    :param region: path of geometry of the region of interest
    :type region: str
    :param ini_config: path to ini config file
    :type ini_config: str
    :param data_libs: optional data libraries , defaults to []
    :type data_libs: list, optional
    :param cli: Boolean indicator for using hydromt cli instead of python
     package, defaults to False
    :type cli: bool, optional
    """
    if not os.path.exists(model_root):
        os.makedirs(model_root)
    starttime = time.time()
    logger = log.setuplog(
        "build", os.path.join(model_root, "hydromt.log"), log_level=10, append=False
    )
    if cli:
        arg_lst = [
            "hydromt",
            "build",
            model,
            model_root,
            region,
            "-i",
            ini_config,
            data_libs,
        ]
        if "deltares_data" in data_libs:
            data_libs.pop(data_libs.index("deltares_data"))
            arg_lst.append("--dd")
        subprocess.run(arg_lst, shell=True)
    else:
        kwargs = dict()
        if "deltares_data" in data_libs:
            data_libs.pop(data_libs.index("deltares_data"))
            kwargs = {"deltares_data": True}
        # TODO logger log_level=10
        logger.info(f"Building instance of {model} model at {model_root}.")
        mod = api_model_plugins().load(api_model_entry_points()[model], logger=logger)(
            root=model_root, mode="w", data_libs=data_libs, logger=logger, **kwargs
        )
        opt = configread(ini_config)
        mod.build(region, opt=opt)
        logger.info(f"Model build finished in {round(time.time()- starttime)} seconds")


def create_variable_threshold_pairs(index: int, var: str = None, thresh: str = None):
    """Creates dash input fields for variable threshold pairs, to be used in model building.

    :param index: integer used for index of the variable threshold pairs
    :type index: int
    :return: Dash Bootstrap row with columns and input fields
    :rtype: dash_bootstrap_components.Row
    """
    if var and thresh:
        return dbc.Row(
            [
                dbc.Col(
                    dbc.Input(id={"type": "variable", "index": index}, value=var),
                    style={
                        "display": "inline-block",
                        "width": "10rem",
                        "margin": "0.5rem auto",
                    },
                ),
                dbc.Col(
                    dbc.Input(id={"type": "threshold", "index": index}, value=thresh),
                    style={
                        "display": "inline-block",
                        "width": "3rem",
                        "margin": "0.5rem auto",
                    },
                ),
            ]
        )

    return dbc.Row(
        [
            dbc.Col(
                dbc.Input(
                    id={"type": "variable", "index": index}, placeholder="Variable"
                ),
                style={
                    "display": "inline-block",
                    "width": "10rem",
                    "margin": "0.5rem auto",
                },
            ),
            dbc.Col(
                dbc.Input(
                    id={"type": "threshold", "index": index}, placeholder="Threshold"
                ),
                style={
                    "display": "inline-block",
                    "width": "3rem",
                    "margin": "0.5rem auto",
                },
            ),
        ]
    )


def get_output_dir() -> str:
    """Creates a default output dir next to the application dir

    :return: path of output dir
    :rtype: str
    """
    app_dir = os.path.dirname(os.path.realpath(__file__))
    dash_dir = os.path.dirname(app_dir)
    output_dir = os.path.join(dash_dir, "output")
    return output_dir


def get_folder(
    title: str = "Please select the folder to place the new project folder in",
) -> str:
    """Opens a file dialog window for choosing a directory.

    :param title: , defaults to "Please select the folder to place the new project folder in"
    :type title: str, optional
    :return: path to chosen directory
    :rtype: str
    """
    root = tkinter.Tk()
    # Force dialog to stay on top of all other open windows - this is the closest we can get to a browser popup.
    root.attributes("-topmost", True)
    # Remove window and task bar
    root.withdraw()
    folder = filedialog.askdirectory(title=title)
    root.destroy()
    return folder if folder else None


def variable_threshold_to_dict(variables: list, thresholds: list) -> dict:
    var_thresh_dict = {}
    for var, thresh in zip(variables, thresholds):
        if var is None or thresh is None:
            continue
        var_thresh_dict[var] = float(thresh)
    return var_thresh_dict


def parse_mapdata(
    map_data: dict,
    model_root: str,
    region_option: str,
    variables: list = None,
    thresholds: list = None,
) -> dict:
    """Parses map data that is generated by drawing a geometry on the map
       and returns a dict with a geometry in the appropriate format

    :param map_data: dict containing data on drawn geometries
    :type map_data: dict
    :param model_root: path to model root
    :type model_root: str
    :param region_option: name of region options
    :type region_option: str
    :param var_thresh_pairs: dictionary with variable-threshold pairs
    :type var_thresh_pairs: dict
    :return: dict with right geometry format
    :rtype: dict
    """

    geom_type = map_data["features"][0]["properties"]["type"]

    if geom_type == "polygon":
        geom_path = os.path.join(model_root, "geom.geojson")
        shutil.move(
            "./data/geom.geojson", geom_path
        )  # Move polygon file to model root dir
        region_dict = {region_option: geom_path}

    elif geom_type == "marker":
        if len(map_data["features"]) > 1:
            x_list = [x["geometry"]["coordinates"][0] for x in map_data["features"]]
            y_list = [y["geometry"]["coordinates"][1] for y in map_data["features"]]
            region_dict = {region_option: [x_list, y_list]}
        else:
            region_dict = {
                region_option: map_data["features"][0]["geometry"]["coordinates"]
            }

    elif geom_type == "rectangle":
        region_dict = {region_option: get_bbox(map_data)}
    if variables and thresholds:
        var_thresh_pairs = variable_threshold_to_dict(variables, thresholds)
        region_dict.update(var_thresh_pairs)
    return region_dict


def get_log_file(model_root: str) -> str:
    """Gets log file from model root

    :param model_root: path to model root
    :type model_root: str
    :return: content of log file
    :rtype: str
    """
    file = os.path.join(model_root, "hydromt.log")
    with open(file, "r") as f:
        log = f.read()
    return log


def get_bbox(map_data: dict) -> list:
    """Creates a bounding box in min x , min y, max x, max y format from
       a dict containing data on map drawn geometry

    :param map_data: dict containing data on map drawn geometry
    :type map_data: dict
    :return: bounding box in min x , min y, max x, max y format
    :rtype: list
    """
    bounds = map_data["features"][0]["properties"]["_bounds"]
    xmin = bounds[0]["lng"]
    ymin = bounds[0]["lat"]
    xmax = bounds[1]["lng"]
    ymax = bounds[1]["lat"]
    return [xmin, ymin, xmax, ymax]
