import requests


class WeatherForecastTool:
    def __init__(self, api_key: str):
        if not api_key:
            raise EnvironmentError(
                "OPENWEATHERMAP_API_KEY is not set or invalid")

        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def _safe_request(self, endpoint: str, place: str, extra_params=None) -> dict:
        """Internal helper for safe OpenWeather API calls."""
        params = {
            "q": place,
            "appid": self.api_key,
            "units": "metric",  # always Celsius
        }

        if extra_params:
            params.update(extra_params)

        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                raise RuntimeError(
                    f"OpenWeather API failed "
                    f"(status={response.status_code}, body={response.text})"
                )

            try:
                data = response.json()
            except ValueError as e:
                raise RuntimeError(
                    f"Invalid JSON response from OpenWeather: {response.text}"
                ) from e

            return data

        except requests.RequestException as e:
            raise RuntimeError(
                f"Network error while calling OpenWeather API: {e}"
            ) from e

    def get_current_weather(self, place: str) -> dict:
        """Get current weather of a place."""
        return self._safe_request("weather", place)

    def get_forecast_weather(self, place: str) -> dict:
        """Get weather forecast of a place."""
        return self._safe_request(
            "forecast",
            place,
            extra_params={"cnt": 10},
        )
