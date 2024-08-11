from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from database.database import get_cities_db, get_city_forecast_db
from main import get_weather_data
from typing import List
from datetime import datetime, date
from statistics import mean
from exceptions import CityNotFoundError, DateNotFoundError


app = FastAPI()


class City(BaseModel):
    list_cities: List[str]


class CityForecast(BaseModel):
    city: str
    country: str
    avg_temperature: float
    forecasts_dates: List[str]


class DetailedForecast(BaseModel):
    date: str
    temp: float
    humidity: int
    wind_speed: float


class Weather(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Main(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    sea_level: int
    grnd_level: int
    humidity: int
    temp_kf: int


class Clouds(BaseModel):
    all: int


class Wind(BaseModel):
    speed: float
    deg: int
    gust: float


class Sys(BaseModel):
    pod: str


class WeatherForecast(BaseModel):
    dt: int
    main: Main
    weather: List[Weather]
    clouds: Clouds
    wind: Wind
    visibility: int
    pop: float
    sys: Sys
    dt_txt: str


@app.get("/cities", response_model=City)
async def get_cities():
    data = get_cities_db()
    return City(list_cities=data)


@app.get("/forecast/{city}", response_model=CityForecast)
async def get_city_forecast(city: str):
    """Get weather forecast for a specific city"""
    data = await get_city_forecast_db(city)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City '{city}' not found"
        )

    # Getting the current date
    today = date.today()

    # We filter forecasts starting from today
    filtered_forecasts = [
        forecast for forecast in data['forecasts']
        if forecast['date'].date() >= today
    ]

    # Calculate the average temperature
    avg_temp = mean(forecast['temperature'] for forecast in filtered_forecasts)

    # Format dates
    formatted_dates = [
        forecast['date'].strftime('%Y-%m-%d %H:%M:%S')
        for forecast in filtered_forecasts
    ]

    return CityForecast(
        city=data['city'],
        country=data['country'],
        avg_temperature=round(float(avg_temp), 2),
        forecasts_dates=formatted_dates
    )


@app.get("/forecast/{city}/{date}", response_model=WeatherForecast)
async def get_weather(city: str, date: str):
    """Get weather forecast for a specific city and date"""
    try:
        # Validate the date format
        forecast_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect date format. Expected format: YYYY-MM-DD HH:MM:SS"
        )

    try:
        data = await get_weather_data(city, date)
    except CityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City '{city}' not found"
        )
    except DateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No weather data found for date '{date}' in city '{city}'"
        )
    return WeatherForecast(
        dt=data['dt'],
        main=Main(**data['main']),
        weather=[Weather(**w) for w in data['weather']],
        clouds=Clouds(**data['clouds']),
        wind=Wind(**data['wind']),
        visibility=data['visibility'],
        pop=data['pop'],
        sys=Sys(**data['sys']),
        dt_txt=data['dt_txt']
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
