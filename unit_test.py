import unittest
from database.database import get_cities_db
import requests
import datetime
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class TestDatabase(unittest.TestCase):
    def test_get_cities_db(self):
        cities = get_cities_db()
        self.assertIsInstance(cities, list)
        self.assertGreater(len(cities), 0)


class TestForecastAPI(unittest.TestCase):
    def test_forecast_api(self):
        base_url = "http://127.0.0.1:8000/forecast/Sydney/"

        # Get the current date and time
        now = datetime.datetime.now()

        # Round up to the next 3-hour interval
        forecast_time = now.replace(hour=now.hour - now.hour % 3, minute=0, second=0, microsecond=0)

        # If the current time has already passed, take the next 3-hour interval
        if forecast_time <= now:
            forecast_time += datetime.timedelta(hours=3)

        # Convert the time into a string of the required format
        forecast_time_str = forecast_time.strftime("%Y-%m-%d %H:%M:%S")
        url = base_url + forecast_time_str

        # Выполнение запроса
        response = requests.get(url)

        # Проверка статус-кода
        self.assertEqual(response.status_code, 200)

        # Получение данных
        data = response.json()

        # Проверка структуры и типов данных
        self.assertIsInstance(data, dict)
        self.assertIn('dt', data)
        self.assertIsInstance(data['dt'], int)

        self.assertIn('main', data)
        self.assertIsInstance(data['main'], dict)
        self.assertIn('temp', data['main'])
        self.assertIsInstance(data['main']['temp'], (int, float))

        self.assertIn('weather', data)
        self.assertIsInstance(data['weather'], list)
        self.assertGreater(len(data['weather']), 0)
        self.assertIsInstance(data['weather'][0], dict)
        self.assertIn('id', data['weather'][0])
        self.assertIn('main', data['weather'][0])
        self.assertIn('description', data['weather'][0])
        self.assertIn('icon', data['weather'][0])

        self.assertIn('clouds', data)
        self.assertIsInstance(data['clouds'], dict)
        self.assertIn('all', data['clouds'])

        self.assertIn('wind', data)
        self.assertIsInstance(data['wind'], dict)
        self.assertIn('speed', data['wind'])
        self.assertIn('deg', data['wind'])

        self.assertIn('visibility', data)
        self.assertIsInstance(data['visibility'], int)

        self.assertIn('pop', data)
        self.assertIsInstance(data['pop'], (int, float))

        self.assertIn('sys', data)
        self.assertIsInstance(data['sys'], dict)

        self.assertIn('dt_txt', data)
        self.assertIsInstance(data['dt_txt'], str)

        # Проверка, что время в ответе соответствует запрошенному времени
        response_time = datetime.datetime.strptime(data['dt_txt'], "%Y-%m-%d %H:%M:%S")
        self.assertEqual(response_time, forecast_time)

        # Вывод полученных данных для проверки
        print(f"Запрошенное время: {forecast_time_str}")
        print(f"Полученные данные: {data}")


class TestDatabaseTable(unittest.TestCase):
    def test_table_exists(self):
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="test",
            database="mydatabase"
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'cities');")
        exists = cur.fetchone()[0]

        self.assertTrue(exists, f"Таблица 'Cities' не найдена. Результат запроса: {exists}")


if __name__ == '__main__':
    unittest.main()
