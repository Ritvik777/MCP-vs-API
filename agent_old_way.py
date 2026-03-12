"""
THE OLD WAY — Call an API directly.

This fetches a weather forecast by talking to the
National Weather Service API ourselves. We handle
everything: URLs, headers, parsing, formatting.
"""

import httpx

# 1. Hit the API with our coordinates
response = httpx.get(
    "https://api.weather.gov/points/37.7749,-122.4194",
    headers={"User-Agent": "weather-app/1.0"},
)
forecast_url = response.json()["properties"]["forecast"]

# 2. Get the actual forecast
forecast = httpx.get(
    forecast_url,
    headers={"User-Agent": "weather-app/1.0"},
).json()

# 3. Print the first period
period = forecast["properties"]["periods"][0]
print(f"{period['name']}: {period['temperature']}°{period['temperatureUnit']}")
print(period["detailedForecast"])
