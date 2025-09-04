from fastapi import APIRouter, Depends
from ..schemas import WeatherResponse
from ..weather import fetch_weather
from ..auth import get_current_user
from ..models import User

router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("/{city}", response_model=WeatherResponse)
async def get_weather(city: str, country: str = "US", current_user: User = Depends(get_current_user)):
    return await fetch_weather(city, country)