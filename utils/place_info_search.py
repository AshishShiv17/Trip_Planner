import os
from langchain_tavily import TavilySearch
from langchain_google_community import GooglePlacesTool, GooglePlacesAPIWrapper


MAX_CHARS = 1500  # prevent token bloat


class GooglePlaceSearchTool:
    def __init__(self, api_key: str):
        if not api_key:
            raise EnvironmentError("GPLACES_API_KEY is not set")

        self.places_wrapper = GooglePlacesAPIWrapper(gplaces_api_key=api_key)
        self.places_tool = GooglePlacesTool(api_wrapper=self.places_wrapper)

    def _safe_run(self, query: str) -> str:
        """Safely run a Google Places query."""
        try:
            result = self.places_tool.run(query)

            if not result:
                raise RuntimeError("Empty response from Google Places")

            return self._normalize_output(result)

        except Exception as e:
            raise RuntimeError(f"Google Places API failed: {e}") from e

    @staticmethod
    def _normalize_output(result) -> str:
        """Ensure output is a clean, truncated string."""
        text = str(result)

        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS] + "..."

        return text

    def google_search_attractions(self, place: str) -> str:
        """Search attractions in the specified place."""
        return self._safe_run(f"top attractive places in and around {place}")

    def google_search_restaurants(self, place: str) -> str:
        """Search restaurants in the specified place."""
        return self._safe_run(
            f"top 10 restaurants and eateries in and around {place}"
        )

    def google_search_activity(self, place: str) -> str:
        """Search popular activities in the specified place."""
        return self._safe_run(f"popular activities in and around {place}")

    def google_search_transportation(self, place: str) -> str:
        """Search transportation options in the specified place."""
        return self._safe_run(
            f"modes of transportation available in {place}"
        )


class TavilyPlaceSearchTool:
    def __init__(self):
        self.tavily_tool = TavilySearch(
            topic="general",
            include_answer="advanced",
        )

    def _safe_run(self, query: str) -> str:
        """Safely run a Tavily query."""
        try:
            result = self.tavily_tool.invoke({"query": query})

            if isinstance(result, dict) and result.get("answer"):
                text = result["answer"]
            else:
                text = str(result)

            if not text:
                raise RuntimeError("Empty response from Tavily")

            return self._normalize_output(text)

        except Exception as e:
            raise RuntimeError(f"Tavily search failed: {e}") from e

    @staticmethod
    def _normalize_output(text: str) -> str:
        """Ensure output is a clean, truncated string."""
        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS] + "..."

        return text

    def tavily_search_attractions(self, place: str) -> str:
        """Search attractions using Tavily."""
        return self._safe_run(f"top attractive places in and around {place}")

    def tavily_search_restaurants(self, place: str) -> str:
        """Search restaurants using Tavily."""
        return self._safe_run(
            f"top 10 restaurants and eateries in and around {place}"
        )

    def tavily_search_activity(self, place: str) -> str:
        """Search activities using Tavily."""
        return self._safe_run(f"popular activities in and around {place}")

    def tavily_search_transportation(self, place: str) -> str:
        """Search transportation using Tavily."""
        return self._safe_run(
            f"modes of transportation available in {place}"
        )
