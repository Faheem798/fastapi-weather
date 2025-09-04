import httpx
from fastapi import HTTPException
from .config import settings
import json
from datetime import datetime

async def fetch_weather(city: str, country: str = "US"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")

    data = response.json()
    curated = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
    }

    # Fetch forecast separately
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        forecast_resp = await client.get(forecast_url)
        if forecast_resp.status_code == 200:
            forecast_data = forecast_resp.json()["list"]
            curated["forecast_summary"] = [
                {"date": item["dt_txt"], "temp": item["main"]["temp"]} for item in forecast_data[:5]  # First 5 (3-hour intervals)
            ]
        else:
            curated["forecast_summary"] = []

    return curated