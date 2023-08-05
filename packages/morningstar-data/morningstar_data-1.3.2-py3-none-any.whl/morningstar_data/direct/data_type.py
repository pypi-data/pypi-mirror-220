"""
Public method parameter and return types
"""
from __future__ import annotations
from enum import Enum

from ._data_type import RaiseEnum


class Universe:
    def __init__(self, n: str, u: str):
        self.name = n
        self.universe_id = u


class Frequency(str, Enum, metaclass=RaiseEnum):
    def __new__(cls, value: str, data_point_id: str) -> Frequency:
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj

    def __init__(self, value: str, data_point_id: str) -> None:
        self.data_point_id = data_point_id

    daily = (
        "daily",
        "HS793",
    )
    weekly = (
        "weekly",
        "HP002",
    )
    monthly = (
        "monthly",
        "HP010",
    )
    quarterly = (
        "quarterly",
        "HP020",
    )
    yearly = (
        "yearly",
        "HS803",
    )


class Blank(str, Enum, metaclass=RaiseEnum):
    warning = ("warning",)
    ignore = ("ignore",)
    update = ("update",)

    @classmethod
    def options(cls) -> str:
        return ", ".join(cls._member_map_.keys())


class PeerGroupMethodology(str, Enum):
    MORNINGSTAR = ("MORNINGSTAR",)
    SIMPLE = ("SIMPLE",)


class Order(str, Enum):
    ASC = ("ASC",)
    DESC = ("DESC",)
