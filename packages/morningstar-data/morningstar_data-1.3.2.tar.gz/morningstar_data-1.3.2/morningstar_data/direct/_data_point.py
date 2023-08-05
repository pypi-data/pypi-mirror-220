import simplejson as json

from pandas import DataFrame
from typing import List, Dict, Any

from . import _decorator
from .._base import _logger
from ._exceptions import ValueErrorException
from ._api import _direct_api_request
from ._config import _Config

_config = _Config()


def _data_point_request_builder(data_point_details: list) -> List[Any]:
    if not data_point_details:
        raise ValueErrorException("No datapoint available.")
    url = f"{_config.data_point_service_url()}v1/datapoints/datapointrequestbuilder"
    response_json: List[Any] = _direct_api_request("POST", url, json.dumps(data_point_details, ignore_nan=True))
    return response_json


def _request_asset_flow_data_points() -> List[Any]:
    url = f"{_config.securitydata_service_url()}v1/assetflow/datapoints"
    response_json: List[Any] = _direct_api_request("GET", url)
    return response_json


def _get_asset_flow_data_points_by_ids(data_point_ids: list) -> list:
    response_json = _request_asset_flow_data_points()
    result = []
    if response_json and isinstance(response_json, list):
        data_point_id_settings_dict = {x.get("datapointId", "").strip(): x for x in response_json if x is not None}
        for data_point_id in data_point_ids:
            settings = data_point_id_settings_dict.get(data_point_id)
            if settings is not None:
                settings = settings.copy()
                settings["datapointName"] = settings.pop("name")
                settings["alias"] = settings["datapointName"]
                result.append(settings)
    return result


@_decorator.error_handler
def _get_data_point_details(params: list) -> List[Dict[Any, Any]]:
    url = f"{_config.data_point_service_url()}v1/datapoints/detail"
    response_json: List[Dict[Any, Any]] = _direct_api_request("POST", url, json.dumps(params, ignore_nan=True))
    data_point_id_list = [
        "OS010",
        "OS01Z",
        "OS245",
    ]  # This is a temporary list of faulty data points. These datapoints will be removed in the future after which we wont have to specifically check for these data points.
    filtered_json_response: List[Dict[Any, Any]] = list(
        filter(lambda x: x.get("canBeAddedToDataset", False) or x["datapointId"] in data_point_id_list, response_json)
    )
    return filtered_json_response


@_decorator.error_handler
def _get_all_universes() -> DataFrame:
    url = f"{_config.data_point_service_url()}v1/universes"
    response_json = _direct_api_request("GET", url)
    result = DataFrame(response_json)
    return result[["id", "name"]]
