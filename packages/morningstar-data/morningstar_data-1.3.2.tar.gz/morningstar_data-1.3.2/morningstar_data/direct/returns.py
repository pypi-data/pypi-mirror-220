import pandas as pd
import numpy as np
import warnings
from typing import List, Optional, Union, List, Dict, Any

from . import _decorator, lookup
from ..direct import investment
from ._exceptions import BadRequestException, ResourceNotFoundError
from . import _error_messages
from .data_type import Frequency
from ._config_key import FORMAT_DATE


@_decorator.typechecked
def returns(
    investments: Union[List[str], str, Dict[str, Any]],
    start_date: str = "2020-01-01",
    end_date: Optional[str] = None,
    freq: Union[Frequency, str] = Frequency.monthly,
    currency: Optional[str] = None,
) -> pd.DataFrame:
    warnings.warn(
        "The returns function is deprecated and will be removed in the next major version. Use get_returns instead",
        FutureWarning,
        stacklevel=2,
    )
    return get_returns(investments, start_date, end_date, freq, currency)


@_decorator.typechecked
def get_returns(
    investments: Union[List[str], str, Dict[str, Any]],
    start_date: str = "2020-01-01",
    end_date: Optional[str] = None,
    freq: Union[Frequency, str] = Frequency.monthly,
    currency: Optional[str] = None,
) -> pd.DataFrame:
    """A shortcut function to fetch return data for the specified investments.

    Args:
        investments (:obj:`Union`, `required`): Defines the investments to fetch. Input can be:

            * Investment IDs (:obj:`list`, `optional`): Investment identifiers, in the format of SecId;Universe or just SecId. E.g., ["F00000YOOK;FO","FOUSA00CFV;FO"] or ["F00000YOOK","FOUSA00CFV"]. Use the `investments <./lookup.html#morningstar_data.direct.investments>`_ function to discover identifiers.
            * Investment List ID (:obj:`str`, `optional`): Saved investment list in Morningstar Direct. Use the `get_investment_lists <./lists.html#morningstar_data.direct.user_items.get_investment_lists>`_ function to discover saved lists.
            * Search Criteria  ID (:obj:`str`, `optional`): Saved search criteria in Morningstar Direct. Use the `get_search_criteria <./search_criteria.html#morningstar_data.direct.user_items.get_search_criteria>`_ function to discover saved search criteria.
            * Search Criteria Condition (:obj:`dict`, `optional`): Search criteria definition. See details in the Reference section of `get_investment_data <#morningstar_data.direct.get_investment_data>`_ or use the `get_search_criteria_conditions <./search_criteria.html#morningstar_data.direct.user_items.get_search_criteria_conditions>`_ function to discover the definition of a saved search criteria.

        start_date (:obj:`str`): Start date of a date range for retrieving data. The format is
            YYYY-MM-DD, e.g., "2020-01-01".
        end_date (:obj:`str`, `optional`): End date of a date range for retrieving data. If no value is provided for
            end_date, current date will be used. The format is YYYY-MM-DD, e.g., "2020-01-01".
        freq (:obj:`Frequency`): Enumeration of return frequency, which can be 'daily', 'weekly', 'monthly', 'quarterly', or 'yearly'. E.g., "md.direct.Frequency.monthly"
        currency (:obj:`str`, `optional`): Three character code for the desired currency of returns, e.g., "USD".  Use the `currency_codes <./lookup.html#morningstar_data.lookup.currency_codes>`_ function to discover possible values.

    Returns:
        DataFrame: A DataFrame object with returns data.

    Examples:
        Get monthly returns.

    ::

        import morningstar_data as md


        df = md.direct.get_returns(
            investments=["F00000VKPI", "F000014B1Y"], start_date="2020-10-01", freq=md.direct.Frequency.monthly
        )
        df

    :Output:
        ==========  ====================================  ======================================
        Name          (LF) FoF Bal Blnd US Priv Banking     (LF) High Yield A List Priv Banking
        ==========  ====================================  ======================================
        2020-10-31     -2.121865                             -0.686248
        2020-11-30     6.337255                              5.682299
        2020-12-31     1.464777                              3.011518
        ...
        ==========  ====================================  ======================================

    Errors:
        AccessDeniedError: Raised when the user is not properly authenticated.

        BadRequestError: Raised when the user does not provide a properly formatted request.

        ForbiddenError: Raised when the user lacks permission to access a resource.

        InternalServerError: Raised when the server encounters an unhandled error.

        NetworkExceptionError: Raised when the request fails to reach the server due to a network error.

        ResourceNotFoundError: Raised when the requested resource does not exist in Direct.

    """

    if not isinstance(freq, Frequency):
        warnings.warn(
            "The use of string values for the 'freq' parameter is deprecated and will be removed in the next major version. Use Frequency enum values instead",
            FutureWarning,
            stacklevel=2,
        )

    freq = Frequency[freq]
    assert isinstance(freq, Frequency)

    start_date = pd.to_datetime(start_date).strftime(FORMAT_DATE)
    data_point_details = lookup.get_data_point_settings(data_point_ids=[freq.data_point_id, "OS01W"]).copy()
    if data_point_details.empty:
        raise BadRequestException("Failed to retrieve datapoint details.")

    # Remove single period timeseries data (due to id collision)
    data_point_details = data_point_details.loc[(data_point_details["datapointId"].isin(["OS01W"])) | (data_point_details["isTsdp"])]
    data_point_details["startDate"] = start_date
    data_point_details["currency"] = currency
    if end_date:
        end_date = pd.to_datetime(end_date).strftime(FORMAT_DATE)
        data_point_details["endDate"] = end_date

    return_value = investment.get_investment_data(investments=investments, data_points=data_point_details)

    if return_value is None or return_value.empty:
        raise ResourceNotFoundError(_error_messages.RESOURCE_NOT_FOUND_ERROR_NO_RETURNS_RETRIEVED)
    if "Id" in return_value.columns:
        return_value = return_value.drop(["Id"], axis=1)
    return_value = return_value.replace(r"^\s*$", None, regex=True)

    if return_value.empty:
        raise ResourceNotFoundError(_error_messages.RESOURCE_NOT_FOUND_ERROR_NO_RETURNS_RETRIEVED_FOR_INVESTMENT_LIST)

    df = return_value.T
    df.columns = df.iloc[-1]
    df.drop(df.tail(1).index, inplace=True)
    new_index = {x: pd.to_datetime(x[-10:]) for x in df.index}
    df = df.rename(index=new_index)
    return df


@_decorator.typechecked
def excess_returns(
    investments: Union[List, str, Dict[str, Any]],
    benchmark_sec_id: str,
    start_date: str = "2020-01-01",
    end_date: Optional[str] = None,
    freq: Union[Frequency, str] = Frequency.monthly,
    currency: Optional[str] = None,
) -> pd.DataFrame:
    warnings.warn(
        "The excess_returns function is deprecated and will be removed in the next major version. Use get_excess_returns instead",
        FutureWarning,
        stacklevel=2,
    )
    return get_excess_returns(investments, benchmark_sec_id, start_date, end_date, freq, currency)


@_decorator.typechecked
def get_excess_returns(
    investments: Union[List, str, Dict[str, Any]],
    benchmark_sec_id: str,
    start_date: str = "2020-01-01",
    end_date: Optional[str] = None,
    freq: Union[Frequency, str] = Frequency.monthly,
    currency: Optional[str] = None,
) -> pd.DataFrame:
    """A shortcut function to fetch excess return data for the specified investments.

    Args:
        investments (:obj:`Union`, `required`): Defines the investments to fetch. Input can be:

            * Investment IDs (:obj:`list`, `optional`): Investment identifiers, in the format of SecId;Universe or just SecId. E.g., ["F00000YOOK;FO","FOUSA00CFV;FO"] or ["F00000YOOK","FOUSA00CFV"]. Use the `investments <./lookup.html#morningstar_data.direct.investments>`_ function to discover identifiers.
            * Investment List ID (:obj:`str`, `optional`): Saved investment list in Morningstar Direct. Use the `get_investment_lists <./lists.html#morningstar_data.direct.user_items.get_investment_lists>`_ function to discover saved lists.
            * Search Criteria  ID (:obj:`str`, `optional`): Saved search criteria in Morningstar Direct. Use the `get_search_criteria <./search_criteria.html#morningstar_data.direct.user_items.get_search_criteria>`_ function to discover saved search criteria.
            * Search Criteria Condition (:obj:`dict`, `optional`): Search criteria definition. See details in the Reference section of `get_investment_data <#morningstar_data.direct.get_investment_data>`_ or use the `get_search_criteria_conditions <./search_criteria.html#morningstar_data.direct.user_items.get_search_criteria_conditions>`_ function to discover the definition of a saved search criteria.

        benchmark_sec_id (:obj:`str`): SecId of the security to use as the benchmark. Use the `investments <./lookup.html#morningstar_data.direct.investments>`_ function to discover identifiers.
        start_date (:obj:`str`): Start date of a date range for retrieving data. The format is
            YYYY-MM-DD, e.g., "2020-01-01".
        end_date (:obj:`str`, `optional`): End date of a date range for retrieving data. If no value is provided for
            end_date, current date will be used. The format is YYYY-MM-DD, e.g., "2020-01-01".
        freq (:obj:`Frequency`): Enumeration of return frequency, which can be 'daily', 'weekly', 'monthly', 'quarterly', or 'yearly'. E.g., "md.direct.Frequency.monthly"
        currency (:obj:`str`, `optional`): Three character code for the desired currency of returns, e.g., "USD".  Use the `currency_codes <./lookup.html#morningstar_data.lookup.currency_codes>`_ function to discover possible values.


    Returns:
        DataFrame: A DataFrame object with excess return data.

    Examples:
        Get monthly excess returns.

    ::

        import morningstar_data as md

        df = md.direct.get_excess_returns(
            investments=["F00000VKPI", "F000014B1Y"],
            benchmark_sec_id="F00000PLYW",
            freq=md.direct.Frequency.daily
        )
        df

    :Output:
        ==========  ====================================  ======================================
        Name          (LF) FoF Bal Blnd US Priv Banking     (LF) High Yield A List Priv Banking
        ==========  ====================================  ======================================
        2020-01-01     -1150.623143                          -1154.382165
        2020-01-02     -1146.064892                          -1149.928106
        ...
        ==========  ====================================  ======================================

    Errors:
        AccessDeniedError: Raised when the user is not authenticated.

        BadRequestError: Raised when the user does not provide a properly formatted request.

        ForbiddenError: Raised when the user does not have permission to access the requested resource.

        InternalServerError: Raised when the server encounters an unhandled error.

        NetworkExceptionError: Raised when the request fails to reach the server due to a network error.

        ResourceNotFoundError: Raised when the requested resource does not exist in Direct.

    """
    if not isinstance(freq, Frequency):
        warnings.warn(
            "The use of string values for the 'freq' parameter is deprecated and will be removed in the next major version. Use Frequency enum values instead",
            FutureWarning,
            stacklevel=2,
        )

    df = get_returns(
        investments=investments,
        start_date=start_date,
        end_date=end_date,
        freq=freq,
        currency=currency,
    )

    if df is None or df.empty:
        raise ResourceNotFoundError(_error_messages.RESOURCE_NOT_FOUND_ERROR_NO_RETURNS_RETRIEVED)

    benchmark_returns = get_returns(
        investments=[benchmark_sec_id],
        start_date=start_date,
        end_date=end_date,
        freq=freq,
        currency=currency,
    )

    if benchmark_returns is None or benchmark_returns.empty:
        raise ResourceNotFoundError(_error_messages.RESOURCE_NOT_FOUND_ERROR_NO_RETURNS_RETRIEVED_FOR_BENCHMARK_ID)

    df["benchmark"] = benchmark_returns.iloc[:, 0]

    df = df.sub(df["benchmark"], axis="rows").drop(columns=["benchmark"])
    return df
