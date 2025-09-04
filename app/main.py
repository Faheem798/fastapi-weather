from fastapi import FastAPI, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database import init_db
from .routers import users, weather
from .auth import get_current_user, create_access_token
from .models import User, FavoriteLocation
from .schemas import UserCreate, FavoriteLocationCreate
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .database import get_session
from .weather import fetch_weather
import asyncio
from datetime import timedelta
from sqlalchemy.orm import joinedload  # Add this import

app = FastAPI(title="Weather Dashboard API")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(users.router)
app.include_router(weather.router)

@app.on_event("startup")
async def startup():
    await init_db()

# Web routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("weather.html", {"request": request, "current_user": current_user})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...), session: AsyncSession = Depends(get_session)):
    from .auth import authenticate_user
    user = await authenticate_user(session, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    response = RedirectResponse(url="/weather", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), session: AsyncSession = Depends(get_session)):
    from .auth import get_password_hash, get_user
    if await get_user(session, username):
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already registered"})
    hashed_password = get_password_hash(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout", response_class=HTMLResponse)
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

@app.get("/weather", response_class=HTMLResponse)
async def weather_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("weather.html", {"request": request, "current_user": current_user})

@app.post("/weather", response_class=HTMLResponse)
async def weather_search(request: Request, city: str = Form(...), country: str = Form("US"), current_user: User = Depends(get_current_user)):
    try:
        weather = await fetch_weather(city, country)
        return templates.TemplateResponse("weather.html", {"request": request, "current_user": current_user, "weather": weather})
    except HTTPException as e:
        return templates.TemplateResponse("weather.html", {"request": request, "current_user": current_user, "error": e.detail})

@app.get("/favorites", response_class=HTMLResponse)
async def favorites_page(request: Request, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # Use joinedload to eagerly load favorites
    query = select(User).where(User.id == current_user.id).options(joinedload(User.favorites))
    result = await session.execute(query)
    user = result.unique().scalar_one_or_none()  # Use unique() to avoid duplicate rows
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("favorites.html", {"request": request, "current_user": current_user, "favorites": user.favorites})

@app.post("/favorites", response_class=HTMLResponse)
async def add_favorite(request: Request, city: str = Form(...), country: str = Form("US"), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    db_fav = FavoriteLocation(city=city, country=country, user_id=current_user.id)  # Create FavoriteLocation directly
    session.add(db_fav)
    await session.commit()
    return RedirectResponse(url="/favorites", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/favorites/{fav_id}/delete", response_class=HTMLResponse)
async def delete_favorite(request: Request, fav_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    query = select(FavoriteLocation).where(FavoriteLocation.id == fav_id, FavoriteLocation.user_id == current_user.id)
    result = await session.execute(query)
    fav = result.scalar_one_or_none()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    await session.delete(fav)
    await session.commit()
    return RedirectResponse(url="/favorites", status_code=status.HTTP_303_SEE_OTHER)