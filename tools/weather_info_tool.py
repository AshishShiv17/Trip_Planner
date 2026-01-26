import os
from utils.weather_info import WeatherForecastTool
from langchain.tools import tool
from typing import List
from dotenv import load_dotenv


class WeatherInfoTool:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise EnvironmentError("OPENWEATHERMAP_API_KEY is not set")

        self.weather_service = WeatherForecastTool(self.api_key)
        self.weather_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the weather forecast tool"""

        @tool("get_current_weather")
        def get_current_weather(city: str) -> str:
            """Get current weather for a city."""
            try:
                weather_data = self.weather_service.get_current_weather(city)

                if not weather_data:
                    return f"Could not fetch current weather for {city}"

                temp = weather_data.get("main", {}).get("temp", "N/A")
                desc = weather_data.get("weather", [{}])[
                    0].get("description", "N/A")

                return f"Current weather in {city}: {temp}°C, {desc}"

            except Exception as e:
                return f"Failed to fetch current weather for {city}: {e}"

        @tool("get_weather_forecast")
        def get_weather_forecast(city: str) -> str:
            """Get 5-day weather forecast for a city (daily summary)."""
            try:
                forecast_data = self.weather_service.get_forecast_weather(city)

                if not forecast_data or "list" not in forecast_data:
                    return f"Could not fetch forecast for {city}"

                daily_seen = set()
                forecast_summary = []

                for item in forecast_data["list"]:
                    date = item.get("dt_txt", "").split(" ")[0]
                    if not date or date in daily_seen:
                        continue

                    daily_seen.add(date)

                    temp = item.get("main", {}).get("temp", "N/A")
                    desc = item.get("weather", [{}])[
                        0].get("description", "N/A")

                    forecast_summary.append(
                        f"{date}: {temp}°C, {desc}"
                    )

                    if len(forecast_summary) >= 5:
                        break

                if not forecast_summary:
                    return f"Could not fetch forecast for {city}"

                return (
                    f"Weather forecast for {city} (next 5 days):\n"
                    + "\n".join(forecast_summary)
                )

            except Exception as e:
                return f"Failed to fetch forecast for {city}: {e}"

        return [get_current_weather, get_weather_forecast]
