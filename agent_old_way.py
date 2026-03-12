"""
Traditional API Integration (The Old Way)
==========================================
Fetches weather forecasts by calling the NWS API directly.
This shows the "before MCP" approach — tightly coupled,
hardcoded, and doesn't scale well to many tools.

Run:
    python agent_old_way.py

Note: This script does NOT require an OpenAI key. It demonstrates
the direct API call pattern without the LLM layer so anyone can
run it and see the output.
"""

import httpx

NWS_BASE = "https://api.weather.gov"
HEADERS = {"User-Agent": "weather-app/1.0"}


def get_forecast(latitude: float, longitude: float) -> str:
    """Fetch forecast from NWS — custom code for this specific API."""
    with httpx.Client() as client:
        points = client.get(
            f"{NWS_BASE}/points/{latitude},{longitude}",
            headers=HEADERS,
            timeout=30.0,
        ).json()

        forecast_url = points["properties"]["forecast"]
        forecast = client.get(
            forecast_url,
            headers=HEADERS,
            timeout=30.0,
        ).json()

    periods = forecast["properties"]["periods"][:3]
    return "\n---\n".join(
        f"{p['name']}:\n"
        f"  Temperature: {p['temperature']}°{p['temperatureUnit']}\n"
        f"  Wind: {p['windSpeed']} {p['windDirection']}\n"
        f"  {p['detailedForecast']}"
        for p in periods
    )


def get_alerts(state: str) -> str:
    """Fetch active alerts for a US state — another custom integration."""
    with httpx.Client() as client:
        data = client.get(
            f"{NWS_BASE}/alerts/active/area/{state}",
            headers=HEADERS,
            timeout=30.0,
        ).json()

    if not data.get("features"):
        return "No active alerts."

    alerts = []
    for feature in data["features"]:
        props = feature["properties"]
        alerts.append(
            f"Event: {props.get('event', 'Unknown')}\n"
            f"Severity: {props.get('severity', 'Unknown')}\n"
            f"Area: {props.get('areaDesc', 'Unknown')}"
        )
    return "\n---\n".join(alerts)


if __name__ == "__main__":
    print("=" * 50)
    print("THE OLD WAY — Direct API Integration")
    print("=" * 50)

    print("\nFetching forecast for San Francisco (37.77, -122.42)...\n")
    print(get_forecast(37.7749, -122.4194))

    print("\n" + "=" * 50)
    print("\nFetching weather alerts for California...\n")
    print(get_alerts("CA"))
