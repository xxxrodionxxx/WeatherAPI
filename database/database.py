import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from log import logger


def get_db_connection(host="localhost", user="postgres", password="test", database="mydatabase"):
    return psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


def get_data_from_geocoding_db(city):
    """Returns a tuple with city, country, lat, lon from geocoding table or None if not found"""
    try:
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute("SELECT city, country, lat, lon FROM geocoding WHERE city = %s", (city,))
            return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error fetching tuple for city '{city}': {error}")
        return None
    finally:
        if conn:
            conn.close()


def get_cities_db():
    """Returns a list of cities from geocoding table"""
    try:
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute("SELECT city FROM geocoding")
            rows = cur.fetchall()
            cities = [city[0] for city in rows]
            return sorted(cities)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error fetching cities: {error}")
        return []
    finally:
        if conn:
            conn.close()


async def get_city_forecast_db(city_name):
    """Returns a list of forecasts for a given city"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            query = sql.SQL("""
                SELECT 
                    ci.CityName,
                    ci.Country,
                    wf.ForecastDateTime,
                    wf.Temperature
                FROM 
                    WeatherForecasts wf
                JOIN 
                    Cities ci ON wf.CityID = ci.CityID
                WHERE 
                    ci.CityName = %s
                    AND wf.ForecastDateTime >= CURRENT_TIMESTAMP
                ORDER BY 
                    wf.ForecastDateTime;
            """)
            cur.execute(query, (city_name,))
            results = cur.fetchall()

            if results:
                city = results[0][0]
                country = results[0][1]
                forecasts = [{"date": row[2], "temperature": row[3]} for row in results]
                return {
                    "city": city,
                    "country": country,
                    "forecasts": forecasts
                }
            else:
                return None
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error fetching forecast for city '{city_name}': {error}")
        return None
    finally:
        if conn:
            conn.close()


def insert_city_in_DB(city, country, lat, lon):
    """Inserts a new city into the database if it doesn't exist"""
    try:
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM Cities WHERE CityName = %s AND Country = %s AND Lat = %s AND Lon = %s;
            """, (city, country, lat, lon))
            exists = cur.fetchone()[0] > 0

            if not exists:
                cur.execute("""
                    INSERT INTO Cities(CityName, Country, Lat, Lon) VALUES (%s, %s, %s, %s);
                """, (city, country, lat, lon))
                logger.info(f"Inserted city '{city}' into database.")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error inserting city '{city}': {error}")
    finally:
        if conn:
            conn.close()


def update_weather_forecasts(data: list):
    """Updates the weather forecasts in the database"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            values_str = ", ".join(
                cur.mogrify("(%s, %s::TIMESTAMP, %s)", (city, date, temp)).decode('utf-8')
                for city, date, temp in data
            )

            query = sql.SQL("""
                WITH city_data (city_name, forecast_date, temperature) AS (
                    VALUES {values}
                )
                INSERT INTO WeatherForecasts (CityID, ForecastDateTime, Temperature)
                SELECT c.CityID, cd.forecast_date, cd.temperature
                FROM city_data cd
                JOIN Cities c ON cd.city_name = c.CityName
                ON CONFLICT (CityID, ForecastDateTime)
                DO UPDATE SET Temperature = EXCLUDED.Temperature;
            """).format(values=sql.SQL(values_str))

            cur.execute(query)
            conn.commit()
            logger.info("Weather forecasts updated successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error updating weather forecasts: {error}")
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    pass
