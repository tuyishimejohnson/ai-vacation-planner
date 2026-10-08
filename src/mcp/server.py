from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP

# Claude Desktop starts this process outside the repository directory.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from ..tools.countries import get_countries_and_cities as countries_tool
from ..tools.exchange_rate import get_exchange_rate as exchange_rate_tool
from ..tools.places import search_places as places_tool
from ..tools.travel_knowledge import search_travel_knowledge as travel_knowledge_tool
from ..tools.weather import get_current_weather as weather_tool

mcp = FastMCP("vacation-planner")


@mcp.tool()
def get_current_weather(city: str) -> dict:
    """Get current weather conditions for a city."""
    return weather_tool({"city": city})


@mcp.tool()
def search_places(query: str, limit: int = 5) -> dict:
    """Search for attractions, hotels, restaurants, or other places."""
    return places_tool({"query": query, "limit": limit})


@mcp.tool()
def search_travel_knowledge(query: str) -> list:
    """Find travel tips, safety, packing, and transportation guidance."""
    return travel_knowledge_tool({"query": query})


@mcp.tool()
def get_countries_and_cities(query: str) -> dict:
    """Look up a country's basic details and its capital cities."""
    return countries_tool({"query": query})


@mcp.tool()
def get_exchange_rate(
    from_currency: str,
    to_currency: str,
    amount: float | None = None,
) -> dict:
    """Get the exchange rate between currencies and optionally convert an amount."""
    return exchange_rate_tool(
        {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
        }
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
