# Weather Dashboard API

A modern web application built with FastAPI, SQLModel, PostgreSQL, and Jinja2 templates, providing real-time weather data via the OpenWeatherMap API. Features include user authentication, weather search, and favorite city management with a responsive, user-friendly interface styled with Tailwind CSS.

## Features
- **User Authentication**: Register, login, and logout with JWT-based authentication (cookie-based for web, token-based for API).
- **Weather Search**: Fetch real-time weather data and 5-day forecasts for any city using OpenWeatherMap.
- **Favorites Management**: Add and remove favorite cities, stored in PostgreSQL.
- **Responsive UI**: Clean, modern interface with Jinja2 templates and Tailwind CSS.
- **Async Backend**: Built with FastAPI and async SQLModel for high performance.
- **API Documentation**: Interactive Swagger UI for testing endpoints.

## Tech Stack
- **Backend**: FastAPI, Python 3.13, SQLModel, PostgreSQL
- **Frontend**: Jinja2 templates, Tailwind CSS (via CDN)
- **APIs**: OpenWeatherMap
- **Database**: PostgreSQL with asyncpg
- **Authentication**: JWT (python-jose, passlib)
- **Tools**: Alembic (database migrations), Pydantic (settings)

## Setup Instructions

### Prerequisites
- Python 3.13+
- PostgreSQL (recommended via Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=yourpassword postgres`)
- OpenWeatherMap API key (sign up at [openweathermap.org](https://openweathermap.org))

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/weather_dashboard_api.git
   cd weather_dashboard_api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory with the following content:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/weather_db
   OPENWEATHER_API_KEY=your_openweathermap_api_key_here
   JWT_SECRET_KEY=supersecretkeychangeme
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Start the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the application**:
   - Web interface: `http://127.0.0.1:8000/`
   - API documentation: `http://127.0.0.1:8000/docs`

## Usage
- **Web Interface**:
  - **Register**: Create an account at `/register`.
  - **Login**: Log in at `/login` to access protected features.
  - **Weather Search**: Search for weather by city and country at `/weather`.
  - **Favorites**: Add or remove favorite cities at `/favorites`.
  - **Logout**: Log out to clear session.
- **API**:
  - Use Swagger UI (`/docs`) to test endpoints:
    - `POST /users/register`: Create a user.
    - `POST /users/token`: Get a JWT token.
    - `GET /weather/{city}`: Fetch weather data (requires token).
    - `POST /users/favorites` and `GET /users/favorites`: Manage favorite cities.

## Project Structure
```
weather_dashboard_api/
├── app/
│   ├── main.py              # FastAPI app and web routes
│   ├── config.py            # Environment settings
│   ├── database.py          # Database setup
│   ├── models.py            # SQLModel models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # JWT authentication
│   ├── weather.py           # Weather API logic
│   ├── routers/             # API routes (users, weather)
│   ├── templates/           # Jinja2 templates for web UI
│   ├── static/              # CSS/JS files (Tailwind CSS)
│   ├── migrations/          # Alembic migrations for database schema
├── .env                     # Environment variables (not committed)
├── alembic.ini              # Alembic configuration
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
```

## Notes
- **Caching**: Redis caching is disabled for simplicity but can be re-enabled for performance in production.
- **Security**: JWT tokens are stored in `httponly` cookies for web routes to prevent XSS attacks.
- **Scalability**: Async/await is used for database and API calls to ensure high performance.
- **Future Enhancements**: Potential additions include weather icons, forecast charts (Chart.js), and rate limiting (slowapi).

## Contributing
Feel free to fork the repository, create a feature branch, and submit a pull request with improvements.
