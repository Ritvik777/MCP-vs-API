"""
THE MCP WAY — A weather tool server.

This does the same thing as agent_old_way.py, but wraps it
as an MCP server. Any AI (Claude, Cursor, etc.) can discover
and call this tool automatically. No API keys needed.
"""

import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server named "weather"
mcp = FastMCP("weather")


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location."""
    async with httpx.AsyncClient() as client:
        # Get the grid point for this location
        point = await client.get(
            f"https://api.weather.gov/points/{latitude},{longitude}",
            headers={"User-Agent": "weather-app/1.0"},
        )
        forecast_url = point.json()["properties"]["forecast"]

        # Get the actual forecast
        forecast = await client.get(
            forecast_url,
            headers={"User-Agent": "weather-app/1.0"},
        )

    # Return the first 3 periods as text
    periods = forecast.json()["properties"]["periods"][:3]
    return "\n\n".join(
        f"{p['name']}: {p['temperature']}°{p['temperatureUnit']}\n"
        f"{p['detailedForecast']}"
        for p in periods
    )


# Start the server (talks via stdin/stdout)
if __name__ == "__main__":
    mcp.run(transport="stdio")
