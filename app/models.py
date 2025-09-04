from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    favorites: List["FavoriteLocation"] = Relationship(back_populates="user")

class FavoriteLocation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    city: str
    country: str = "US"
    added_at: datetime = Field(default_factory=datetime.utcnow)
    user: User = Relationship(back_populates="favorites")