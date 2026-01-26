import os
from utils.currency_converter import CurrencyConverter
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv


class CurrencyConverterTool:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        if not self.api_key:
            raise EnvironmentError("EXCHANGE_RATE_API_KEY is not set")

        self.currency_service = CurrencyConverter(self.api_key)
        self.currency_converter_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the currency converter tool"""

        @tool("convert_currency")
        def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
            """
            Convert an amount of money from one currency to another.

            Args:
                amount (float): Amount of money to convert
                from_currency (str): Source currency code (e.g., USD, INR)
                to_currency (str): Target currency code (e.g., EUR, JPY)

            Returns:
                float: Converted amount in target currency
            """
            try:
                return self.currency_service.convert(amount, from_currency, to_currency)
            except Exception as e:
                raise RuntimeError(
                    f"Currency conversion failed "
                    f"({amount} {from_currency} → {to_currency}): {e}"
                ) from e

        return [convert_currency]
