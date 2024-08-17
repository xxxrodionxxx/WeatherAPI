# Weather API

This is a FastAPI application that provides weather forecasts for various cities. The API allows you to fetch a list of cities, get weather forecasts for a specific city, and get detailed weather forecasts for a specific city and date.

## Features

- Retrieve a list of all available cities
- Get weather forecast for a specific city
- Get detailed weather forecast for a specific city and date

## Tech Stack

- Python 3.11
- FastAPI - a modern, fast (high-performance) web framework for building APIs with Python
- Uvicorn - a lightning-fast ASGI server
- Pydantic - data validation and settings management using Python type annotations

## Requirements

Ensure you have Python 3.11 or higher installed.

## Installation

1. Clone the repository:
    ```shell
    git clone https://github.com/xxxrodionxxx/WeatherAPI.git
    cd WeatherAPI
    ```
2. Create and activate a virtual environment: To create a virtual environment, execute: 
    ```shell
    python -m venv env
    source env/bin/activate  # For Linux and macOS
    # or
    .\env\Scripts\activate  # For Windows
    ```
3. Install the dependencies: Execute the command:
    ```shell
    pip install -r requirements.txt
    ```
## Running the Application

To start the FastAPI application, use the following command:
    
    uvicorn API:app --host 0.0.0.0 --port 8000 --reload 
    
This will start the server at <http://localhost:8000>. The --reload flag enables auto-reloading of the server when code changes are detected.

## Using the API

Once the server is running, you can interact with the API as follows:

- Get list of cities: GET /cities
- Get weather forecast for a city: GET /forecast/{city}
- Get detailed weather forecast for a city and date: GET /forecast/{city}/{date}

For detailed API documentation and an interactive interface, visit: <http://localhost:8000/docs>

## Development

To add new features or fix bugs, please create a new branch and submit a pull request.

## Contact

If you have any questions or suggestions, please open an issue in this repository or contact us at: <xxxrodionxxx@mail.ru>

