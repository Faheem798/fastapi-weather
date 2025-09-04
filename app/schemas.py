from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class FavoriteLocationCreate(BaseModel):
    city: str
    country: str = "US"

class FavoriteLocationOut(FavoriteLocationCreate):
    id: int
    added_at: datetime

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: int
    description: str
    forecast_summary: List[dict]  # e.g., [{"date": "2025-08-29", "temp": 25.0}]