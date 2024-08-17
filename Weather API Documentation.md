**Weather API Documentation**

**Base URL:**

http://localhost:8000

-----
**Endpoints**

**1. Get List of Cities**

**Endpoint:**

GET /cities

**Description:** Fetch a list of cities available in the database.

**Response:**

- **200 OK**

{

`    `**"list\_cities": [**

`    `**"Bangkok",**

`    `**"Beijing",**

`    `**"Berlin",**

`    `**"Buenos Aires",**

`    `**"Cairo",**

`    `**"Cape Town",**

`    `**"Dubai",**

`    `**"Istanbul",**

`    `**"Lagos",**

`    `**"London",**

`    `**"Los Angeles",**

`    `**"Mexico City",**

`    `**"Moscow",**

`    `**"New York County",**

`    `**"Paris",**

`    `**"Rome",**

`    `**"Seoul",**

`    `**"Shanghai",**

`    `**"Sydney",**

`    `**"Tokyo"**

`  `**]**

}

-----
**2. Get Weather Forecast for a City**

**Endpoint:**

GET /forecast/{city}

**Description:** Fetch weather forecast for a specific city, including average temperature and forecast dates starting from today.

**Path Parameters:**

- **city** (string): Name of the city.

**Response:**

- **200 OK**

{

`  `"city": "Tokyo",

`  `"country": "JP",

`  `"avg\_temperature": 30.25,

`  `"forecasts\_dates": [

`    `"2024-08-11 12:00:00",

`    `"2024-08-11 15:00:00",

`    `"2024-08-11 18:00:00",

…

`  `] }

- **404 Not Found**

{

`    `"detail": "City 'CityName' not found"

}

-----
**3. Get Detailed Weather Forecast for a City on a Specific Date**

**Endpoint:**

GET /forecast/{city}/{date}

**Description:** Fetch detailed weather forecast for a specific city on a specific date.

**Path Parameters:**

- **city** (string): Name of the city.
- **date** (string): Date in the format YYYY-MM-DD HH:MM:SS.

**Response:**

- **200 OK**

{

`    `**"dt": 1723388400,**

`  `**"main": {**

`    `**"temp": 30.6,**

`    `**"feels\_like": 34.25,**

`    `**"temp\_min": 30.6,**

`    `**"temp\_max": 30.6,**

`    `**"pressure": 998,**

`    `**"sea\_level": 998,**

`    `**"grnd\_level": 996,**

`    `**"humidity": 61,**

`    `**"temp\_kf": 0**

`  `**},**

`  `**"weather": [**

`    `**{**

`      `**"id": 500,**

`      `**"main": "Rain",**

`      `**"description": "light rain",**

`      `**"icon": "10n"**

`    `**}**

`  `**],**

`  `**"clouds": {**

`    `**"all": 100**

`  `**},**

`  `**"wind": {**

`    `**"speed": 3.83,**

`    `**"deg": 287,**

`    `**"gust": 7.11**

`  `**},**

`  `**"visibility": 10000,**

`  `**"pop": 0.74,**

`  `**"sys": {**

`    `**"pod": "n"**

`  `**},**

`  `**"dt\_txt": "2024-08-11 15:00:00"**

}

- **400 Bad Request**

json

Копировать код

{

`    `"detail": "Incorrect date format. Expected format: YYYY-MM-DD HH:MM:SS"

}

- **404 Not Found**

json

Копировать код

{

`    `"detail": "City 'CityName' not found"

}

or

{

`    `"detail": "No weather data found for date '2024-08-10 15:00:00' in city 'CityName'"

}

-----
**Data Models**

**City**

**Description:** Model representing a list of cities.

**Fields:**

- **list\_cities** (List[str]): List of city names.
-----
**CityForecast**

**Description:** Model representing weather forecast for a city.

**Fields:**

- **city** (str): Name of the city.
- **country** (str): Country of the city.
- **avg\_temperature** (float): Average temperature.
- **forecasts\_dates** (List[str]): List of forecast dates starting from today.
-----
**DetailedForecast**

**Description:** Model representing detailed weather forecast for a specific date.

**Fields:**

- **date** (str): Date of the forecast.
- **temp** (float): Temperature.
- **humidity** (int): Humidity percentage.
- **wind\_speed** (float): Wind speed.
-----
**Weather**

**Description:** Model representing weather conditions.

**Fields:**

- **id** (int): Weather condition id.
- **main** (str): Group of weather parameters (Rain, Snow, Extreme etc.).
- **description** (str): Weather condition within the group.
- **icon** (str): Weather icon id.
-----
**Main**

**Description:** Model representing main weather data.

**Fields:**

- **temp** (float): Temperature.
- **feels\_like** (float): Temperature as perceived by humans.
- **temp\_min** (float): Minimum temperature.
- **temp\_max** (float): Maximum temperature.
- **pressure** (int): Atmospheric pressure.
- **sea\_level** (int): Atmospheric pressure at sea level.
- **grnd\_level** (int): Atmospheric pressure at ground level.
- **humidity** (int): Humidity percentage.
- **temp\_kf** (int): Temperature coefficient.
-----
**Clouds**

**Description:** Model representing cloud data.

**Fields:**

- **all** (int): Cloudiness percentage.
-----
**Wind**

**Description:** Model representing wind data.

**Fields:**

- **speed** (float): Wind speed.
- **deg** (int): Wind direction in degrees.
- **gust** (float): Wind gust speed.
-----
**Sys**

**Description:** Model representing system data.

**Fields:**

- **pod** (str): Part of the day (n: night, d: day).
-----
**WeatherForecast**

**Description:** Model representing a detailed weather forecast for a specific date and city.

**Fields:**

- **dt** (int): Date and time of the forecast in Unix format.
- **main** (Main): Main weather data.
- **weather** (List[Weather]): List of weather conditions.
- **clouds** (Clouds): Cloud data.
- **wind** (Wind): Wind data.
- **visibility** (int): Visibility in meters.
- **pop** (float): Probability of precipitation.
- **sys** (Sys): System data.
- **dt\_txt** (str): Date and time of the forecast in human-readable format.
-----
**Error Handling**

**HTTP 400 Bad Request:**

- **Description:** Incorrect date format.
- **Example:**

{

`    `"detail": "Incorrect date format. Expected format: YYYY-MM-DD HH:MM:SS"

}

**HTTP 404 Not Found:**

- **Description:** City not found or no forecast available for the specified city and date.
- **Examples:**

{

`    `"detail": "City 'CityName' not found"

}

or

{

`    `"detail": "No weather data found for date '2024-08-10 15:00:00' in city 'CityName'"

}

**HTTP 500 Internal Server Error:**

- **Description:** An unexpected error occurred on the server.
- **Example:**

{

`    `"detail": "Internal server error"

}

-----
**Running the Application**

To run the FastAPI application, use the following command:

uvicorn API:app --host 0.0.0.0 --port 8000

This starts the server and makes the API available at http://localhost:8000.

