import json
import os
import evaluate
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import numpy as np

PROCESSED_DATA_DIR = "data/processed"
MODELS_DIR = "models"
RESULTS_DIR = "results"

def evaluate_model(model_name, test_data):
    """Оценивает модель на тестовых данных."""

    model_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(model_path):
        print(f"Модель {model_name} не найдена. Пропустите оценку.")
        return

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to("cuda" if torch.cuda.is_available() else "cpu")

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    bleu_scores = []
    rouge_scores = []
    smoothie = SmoothingFunction().method4

    for data_point in test_data:
        query = data_point["query"]
        context = data_point.get("context", "")
        reference = data_point.get("answer", "")

        input_text = f"{query} [CONTEXT] {context}"
        inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
        try:
            output = model.generate(**inputs, max_length=150)
            response = tokenizer.decode(output[0], skip_special_tokens=True)
        except Exception as e:
            print(f"Ошибка при генерации для запроса: {query}. Ошибка: {e}")
            continue

        if reference: # only if reference exists
            rouge = scorer.score(reference, response)
            rouge_scores.append(rouge)
            bleu = sentence_bleu([reference.split()], response.split(), smoothing_function=smoothie)
            bleu_scores.append(bleu)

    avg_rouge1 = np.mean([score["rouge1"].fmeasure for score in rouge_scores]) if rouge_scores else 0
    avg_rouge2 = np.mean([score["rouge2"].fmeasure for score in rouge_scores]) if rouge_scores else 0
    avg_rougeL = np.mean([score["rougeL"].fmeasure for score in rouge_scores]) if rouge_scores else 0
    avg_bleu = np.mean(bleu_scores) if bleu_scores else 0

    return {
        "rouge1": avg_rouge1,
        "rouge2": avg_rouge2,
        "rougeL": avg_rougeL,
        "bleu": avg_bleu
    }


def evaluate_models():
    """Оценивает все доступные модели."""
    try:
        with open(os.path.join(PROCESSED_DATA_DIR, "test.json"), "r", encoding="utf-8") as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print("Файл test.json не найден. Создайте тестовый набор данных.")
        return

    os.makedirs(RESULTS_DIR, exist_ok=True)

    results = {}
    for model_name in os.listdir(MODELS_DIR):
        if os.path.isdir(os.path.join(MODELS_DIR, model_name)):  # Проверяем, что это директория
            print(f"Оценка модели: {model_name}")
            model_results = evaluate_model(model_name, test_data)

            if model_results:
                results[model_name] = model_results
                print(f"Результаты оценки {model_name}: {model_results}")

    # Сохранение результатов в JSON
    with open(os.path.join(RESULTS_DIR, "evaluation_results.json"), "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    evaluate_models()