from typing import Union, List

from hydromt import model_plugins
from hydromt.cli.api import get_model_components, get_datasets, get_region
from geojson import FeatureCollection, dump, loads


def api_model_components(model_name: str) -> dict:
    """Get model components from json file

    :param model_name: name of model plugin
    :type model_name: str
    :return: dictionary with model plugin components and meta data
    :rtype: dict
    """
    return get_model_components(model_name)


def api_datasets(data_libs: list) -> dict:
    """Get model components from json file

    :param data_libs: data catalog names or paths
    :type model_name: str
    :return: dictionary with model available datasets
    :rtype: dict
    """
    return get_datasets(data_libs)


def api_model_options() -> list:
    options = [{"label": k, "value": k} for k in model_plugins.get_plugin_eps().keys()]
    return options


def get_component_docs(model_name, method: str):
    """Retrieves the docstring of a given model plugin method

    :param model_name: name of model plugin
    :type model_name: str
    :param method: name of model method (component)
    :type method: str
    :return: docstring of model method
    :rtype: str
    """
    data = api_model_components(model_name)
    docstring = data[method]["doc"]  # .split(".\n")
    return docstring


def api_model_entry_points():
    return model_plugins.get_plugin_eps()


def api_model_plugins():
    return model_plugins


def api_get_region(region: dict, data_libs: Union[List, str]):
    region_geojson = get_region(region, data_libs)
    # save_geojson(feature=region, model_root="./data")

    region_geojson = loads(region_geojson)

    with open("data/preview_region.geojson", "w") as f:
        dump(region_geojson, f)

    return region_geojson
