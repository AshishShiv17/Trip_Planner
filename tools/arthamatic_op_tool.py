from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper
from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@tool
def currency_converter(from_curr: str, to_curr: str, value: float) -> float:
    """Convert currency using real-time Alpha Vantage rates."""
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        raise EnvironmentError("ALPHAVANTAGE_API_KEY is not set")

    os.environ["ALPHAVANTAGE_API_KEY"] = api_key
    alpha_vantage = AlphaVantageAPIWrapper()

    try:
        response = alpha_vantage.get_exchange_rate(from_curr, to_curr)

        rate = float(
            response["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        )

        return value * rate

    except Exception as e:
        raise RuntimeError(
            f"Currency conversion failed ({from_curr} → {to_curr}, value={value}): {e}"
        ) from e
