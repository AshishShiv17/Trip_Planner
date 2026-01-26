import requests


class CurrencyConverter:
    def __init__(self, api_key: str):
        if not api_key:
            raise EnvironmentError(
                "EXCHANGE_RATE_API_KEY is not set or invalid")

        self.api_key = api_key
        self.base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest"

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert the amount from one currency to another using ExchangeRate-API."""
        if amount < 0:
            raise ValueError("Amount must be non-negative")

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        url = f"{self.base_url}/{from_currency}"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                raise RuntimeError(
                    f"ExchangeRate API call failed "
                    f"(status={response.status_code}, body={response.text})"
                )

            data = response.json()

            rates = data.get("conversion_rates")
            if not isinstance(rates, dict):
                raise RuntimeError(
                    f"Invalid API response format: missing 'conversion_rates'. "
                    f"Raw response: {data}"
                )

            if to_currency not in rates:
                raise ValueError(
                    f"{to_currency} not found in exchange rates for {from_currency}."
                )

            return float(amount) * float(rates[to_currency])

        except requests.RequestException as e:
            raise RuntimeError(
                f"Network error while calling ExchangeRate API: {e}"
            ) from e
