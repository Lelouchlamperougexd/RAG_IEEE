from src import rag_utils
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def run_inference(query):
    # ... загрузка модели и токенизатора

    # Получение релевантных контекстов с помощью RAG
    relevant_contexts = rag_utils.retrieve_contexts(query)

    # Формирование входного текста для модели
    input_text = f"{query} [CONTEXT] {' '.join(relevant_contexts)}"

    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_length=150)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response