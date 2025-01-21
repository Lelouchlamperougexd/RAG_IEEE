import json
from src import api_interaction
import os

DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"

def prepare_data():
    """Собирает данные из API и подготавливает датасет."""
    # Загрузка запросов пользователей (пример)
    with open(os.path.join(DATA_DIR, "user_queries.json"), "r", encoding="utf-8") as f:
        user_queries = json.load(f)

    prepared_data = []
    for query_data in user_queries:
        query = query_data["query"]
        coordinates = query_data.get("coordinates")  # Координаты могут быть необязательными

        context = ""
        if coordinates:
            weather_data = api_interaction.get_weather_data("Астана") 
            traffic_data = api_interaction.get_traffic_info(coordinates)

            if weather_data:
                context += f"Погода: {weather_data['weather'][0]['description']}, температура: {weather_data['main']['temp']}°C. "
            if traffic_data:
                # Обработка данных о пробках (пример)
                try:
                    context += f"Пробки: {traffic_data['features'][0]['properties']['times']['current']['time']}."
                except (KeyError, IndexError):
                    context += "Информация о пробках недоступна."
        
        prepared_data.append({
            "query": query,
            "context": context,
            "answer": query_data.get("answer", "")  # Эталонный ответ (если есть)
        })

    # Сохранение обработанных данных
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    with open(os.path.join(PROCESSED_DATA_DIR, "train.json"), "w", encoding="utf-8") as outfile:
        json.dump(prepared_data, outfile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    prepare_data()