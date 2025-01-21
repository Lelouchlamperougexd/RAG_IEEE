import requests
import json
import os

# Получение ключей API из переменных окружения (рекомендуемый способ)
WEATHER_API_KEY = "6d9f8e84-7cbe-4cbd-842b-f7d21e52c36c"
TWOGIS_API_KEY = "6d9f8e84-7cbe-4cbd-842b-f7d21e52c36c"

if not WEATHER_API_KEY:
    raise ValueError("Необходимо установить переменную окружения WEATHER_API_KEY")
if not TWOGIS_API_KEY:
    raise ValueError("Необходимо установить переменную окружения TWOGIS_API_KEY")


def get_weather_data(city):
    """Получает данные о погоде для заданного города."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"  # Пример URL
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",  # Градусы Цельсия
        "lang": "ru" # Русский язык
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к Weather API: {e}")
        return None

def get_traffic_data(coordinates):
    """Получает данные о пробках для заданных координат (широта, долгота)."""
    base_url = "https://catalog.api.2gis.com/3.0/items/geocode" # Пример URL для геокодирования
    params = {
        "q": f"{coordinates[1]},{coordinates[0]}",
        "fields": "items.geometry.centroid,items.address", # Запрашиваем геометрию и адрес
        "key": TWOGIS_API_KEY,
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к 2GIS API: {e}")
        return None

def get_traffic_info(coordinates):
    """Получает информацию о пробках вблизи заданных координат."""
    base_url = "https://traffic.api.2gis.com/1.0/broutes"
    params = {
        "r[0]": f"r{coordinates[1]},{coordinates[0]}",
        "key": TWOGIS_API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к 2GIS API: {e}")
        return None



# Пример использования
if __name__ == "__main__":
    weather_data = get_weather_data("Москва")
    if weather_data:
        print(json.dumps(weather_data, indent=4, ensure_ascii=False))  # Вывод с форматированием

    traffic_data = get_traffic_data([55.75, 37.62]) # Пример координат
    if traffic_data:
        print(json.dumps(traffic_data, indent=4, ensure_ascii=False))

    traffic_info = get_traffic_info([55.75, 37.62])
    if traffic_info:
        print(json.dumps(traffic_info, indent=4, ensure_ascii=False))