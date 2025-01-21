import data_preparation
import model_training
import model_evaluation

# Подготовка данных
train_dataset, val_dataset, test_dataset = data_preparation.prepare_data()

# Обучение моделей
model_training.train_model(train_dataset, val_dataset)

# Оценка моделей
results = model_evaluation.evaluate_models(test_dataset)

# Сохранение результатов
# ...