from contextvars import Token
import datetime
import os
import uuid
import simplejson as json
import logging
import requests
import inspect


from typing import Optional, Union, List, Any, Dict, Callable
from .direct._config import _Config


_config = _Config()
_logger = logging.getLogger(__name__)


def get_parameter(key: str) -> Optional[Any]:
    """Fetch a parameter from query string with a fallback to an environment variable

    Voila supports query string parameters (available via QUERY_STRING environment variable).
    This function helps to prioritize query string parameters over environment variables with matching names.
    """

    try:
        from os import environ as _env
        from urllib.parse import parse_qs

        # Voila supports
        query_string = _env.get("QUERY_STRING", "")
        parameters: Dict[str, Any] = parse_qs(query_string)
        if key in parameters:
            return parameters[key][0]
        if key in _env:
            return _env.get(key)
        return None
    except BaseException:
        _logger.warn(f"Something is wrong with key={key}")
        return None


def load_remote(target_folder: str, remote_endpoint: str) -> Any:
    from os import path as _path
    from subprocess import run

    try:
        result = run(
            [
                "sh",
                _path.join(_path.dirname(__file__), "remote.sh"),
                target_folder,
                remote_endpoint,
            ],
            shell=False,
            capture_output=True,
        )
        return result
    except Exception as _ex:
        _logger.warn(_ex)


def format_analytics_logs(function: str, params: str, component: str = "morningstar_data.direct", action: str = "FUNCTION_RUN") -> str:
    request_id = str(uuid.uuid1())
    result = {
        "object_type": "MD Package",
        "object_id": function,
        "application": "Analytics Lab",
        "component": component,
        "action": action,
        "session_id": os.getenv("ANALYTICSLAB_SESSION_ID"),
        "user_id": os.getenv("UIM_USER_ID"),
        "details": params,
        "event_id": request_id,
    }

    return f"{json.dumps(result, ignore_nan=True)}"


def get_log_flag(func: Callable) -> bool:

    # log_flag allows to know if a function should be logged for analytics or not
    log_flag = True

    # Return a list of frame records for the caller function’s stack. The first entry in the returned list represents the caller; the last entry represents the outermost call on the stack.
    stack = inspect.stack()

    for stk in stack:
        # <module> represents it is for function called by function execution) - should return true
        if stk.function == "<module>":
            return log_flag
        # Checks if caller is any internal function or not get_log_flag (self), sets flag to false
        elif stk.function not in ["get_log_flag", "wrapper"] or stk.function.startswith("_"):
            log_flag = False
            return log_flag
        else:
            continue

    return log_flag
