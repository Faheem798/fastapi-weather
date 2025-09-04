# Weather Dashboard API

A modern web application built with FastAPI, SQLModel, PostgreSQL, and Jinja2 templates, providing weather data via the OpenWeatherMap API. Features include user authentication, weather search, and favorite city management with a responsive UI using Tailwind CSS.

## Features
- **User Authentication**: Register, login, and logout with JWT-based authentication.
- **Weather Search**: Fetch real-time weather data for any city using OpenWeatherMap.
- **Favorites**: Add and remove favorite cities, stored in PostgreSQL.
- **Responsive UI**: Clean, modern interface with Jinja2 templates and Tailwind CSS.
- **Async Backend**: Built with FastAPI and async SQLModel for performance.

## Tech Stack
- **Backend**: FastAPI, Python 3.13, SQLModel, PostgreSQL
- **Frontend**: Jinja2, Tailwind CSS
- **APIs**: OpenWeatherMap
- **Database**: PostgreSQL (with asyncpg)
- **Authentication**: JWT (python-jose, passlib)
- **Tools**: Alembic (migrations), Pydantic (settings)

## Setup Instructions

### Prerequisites
- Python 3.13+
- PostgreSQL (e.g., via Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=yourpassword postgres`)
- OpenWeatherMap API key (sign up at [openweathermap.org](https://openweathermap.org))

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/weather_dashboard_api.git
   cd weather_dashboard_api