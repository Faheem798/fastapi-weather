from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from ..models import User, FavoriteLocation
from ..schemas import UserCreate, UserOut, Token, FavoriteLocationCreate, FavoriteLocationOut
from ..auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from ..database import get_session
from datetime import timedelta
from ..config import settings
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await session.execute(select(User).where(User.username == user.username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/favorites", response_model=FavoriteLocationOut)
async def add_favorite(fav: FavoriteLocationCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    db_fav = FavoriteLocation(**fav.dict(), user_id=current_user.id)
    session.add(db_fav)
    await session.commit()
    await session.refresh(db_fav)
    return db_fav

@router.post("/favorites", response_model=FavoriteLocationCreate)
async def add_favorite(favorite: FavoriteLocationCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    db_fav = FavoriteLocation(city=favorite.city, country=favorite.country, user_id=current_user.id)
    session.add(db_fav)
    await session.commit()
    return favorite