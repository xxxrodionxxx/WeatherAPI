-- Создание таблицы Cities
CREATE TABLE IF NOT EXISTS Cities (
    CityID SERIAL PRIMARY KEY,  -- Первичный ключ
    CityName VARCHAR(100) NOT NULL,  -- Название города (обязательное поле)
    Country VARCHAR(100),  -- Страна
    Lat DECIMAL(6, 2),  -- Широта
    Lon DECIMAL(6, 2)  -- Долгота
);

-- Создание таблицы WeatherForecasts
CREATE TABLE IF NOT EXISTS WeatherForecasts (
    ForecastID SERIAL PRIMARY KEY,  -- Первичный ключ
    CityID INT,  -- Внешний ключ, ссылающийся на CityID в таблице Cities
    ForecastDateTime TIMESTAMP,  -- Время прогноза
    Temperature DECIMAL(5, 2),  -- Температура
    FOREIGN KEY (CityID) REFERENCES Cities(CityID)  -- Внешний ключ
);