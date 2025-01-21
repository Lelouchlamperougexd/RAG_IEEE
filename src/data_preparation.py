import pandas as pd

def prepare_data(data_path):
    """
    Загружает данные из CSV файла и преобразует их в формат, подходящий для модели.

    Args:
        data_path (str): Путь к CSV файлу.

    Returns:
        pandas.DataFrame: DataFrame с подготовленными данными.
    """

    df = pd.read_csv(data_path)

    # Преобразование категориальных признаков в числовые (если необходимо)
    # ...

    # Создание столбца с объединенным запросом
    df['combined_query'] = df['начальная_точка'] + ' ' + df['конечная_точка'] + ' ' + df['пробки'] + ' ' + df['погода']

    return df