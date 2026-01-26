import os
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv


class PlaceSearchTool:
    def __init__(self):
        load_dotenv()

        self.google_api_key = os.getenv("GPLACES_API_KEY")

        if not self.google_api_key:
            print(
                "⚠️ GPLACES_API_KEY not set — Google Places disabled, using Tavily only")
            self.google_places_search = None
        else:
            self.google_places_search = GooglePlaceSearchTool(
                self.google_api_key)

        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""

        @tool("search_attractions")
        def search_attractions(place: str) -> str:
            """Search tourist attractions in a place."""
            try:
                if self.google_places_search:
                    result = self.google_places_search.google_search_attractions(
                        place)
                    if result:
                        return (
                            f"Following are the attractions of {place} "
                            f"as suggested by Google:\n{result}"
                        )

                tavily_result = self.tavily_search.tavily_search_attractions(
                    place)
                return (
                    f"Google returned no results.\n"
                    f"Following are the attractions of {place} (via Tavily):\n{tavily_result}"
                )

            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_attractions(
                    place)
                return (
                    f"Google failed due to: {e}\n"
                    f"Following are the attractions of {place} (via Tavily):\n{tavily_result}"
                )

        @tool("search_restaurants")
        def search_restaurants(place: str) -> str:
            """Search restaurants in a place."""
            try:
                if self.google_places_search:
                    result = self.google_places_search.google_search_restaurants(
                        place)
                    if result:
                        return (
                            f"Following are the restaurants of {place} "
                            f"as suggested by Google:\n{result}"
                        )

                tavily_result = self.tavily_search.tavily_search_restaurants(
                    place)
                return (
                    f"Google returned no results.\n"
                    f"Following are the restaurants of {place} (via Tavily):\n{tavily_result}"
                )

            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_restaurants(
                    place)
                return (
                    f"Google failed due to: {e}\n"
                    f"Following are the restaurants of {place} (via Tavily):\n{tavily_result}"
                )

        @tool("search_activities")
        def search_activities(place: str) -> str:
            """Search activities in and around a place."""
            try:
                if self.google_places_search:
                    result = self.google_places_search.google_search_activity(
                        place)
                    if result:
                        return (
                            f"Following are the activities in and around {place} "
                            f"as suggested by Google:\n{result}"
                        )

                tavily_result = self.tavily_search.tavily_search_activity(
                    place)
                return (
                    f"Google returned no results.\n"
                    f"Following are the activities of {place} (via Tavily):\n{tavily_result}"
                )

            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_activity(
                    place)
                return (
                    f"Google failed due to: {e}\n"
                    f"Following are the activities of {place} (via Tavily):\n{tavily_result}"
                )

        @tool("search_transportation")
        def search_transportation(place: str) -> str:
            """Search transportation options in a place."""
            try:
                if self.google_places_search:
                    result = self.google_places_search.google_search_transportation(
                        place)
                    if result:
                        return (
                            f"Following are the modes of transportation available in {place} "
                            f"as suggested by Google:\n{result}"
                        )

                tavily_result = self.tavily_search.tavily_search_transportation(
                    place)
                return (
                    f"Google returned no results.\n"
                    f"Following are the modes of transportation available in {place} "
                    f"(via Tavily):\n{tavily_result}"
                )

            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_transportation(
                    place)
                return (
                    f"Google failed due to: {e}\n"
                    f"Following are the modes of transportation available in {place} "
                    f"(via Tavily):\n{tavily_result}"
                )

        return [
            search_attractions,
            search_restaurants,
            search_activities,
            search_transportation,
        ]
