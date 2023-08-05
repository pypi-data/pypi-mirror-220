from enum import Enum
from typing import Any


class PortfolioType(Enum):
    def __init__(self, save_key: str, get_key: str, abbr: str) -> None:
        self.save_key = save_key
        self.get_key = get_key
        self.abbr = abbr

    @classmethod
    def get_full_name_by_abbr(cls, abbr: str) -> str:
        # Api return values are "MD","AC","BM","UA",we use abbr to get portfolio type full name.
        for member in cls._member_map_.values():
            if member._value_[2] == abbr:
                return member.name
        return ""

    # The first value is used to create portfolio(transaction_accounts not supported).
    # The second value is used to get portfolio list.
    # The third value is portfolio list response,we can use this to get portfolio type full name .
    model_portfolios = ("60", "1", "MD")
    custom_benchmarks = ("63", "2", "BM")
    client_accounts = ("90", "0", "UA")
    transaction_accounts = ("", "0", "AC")
