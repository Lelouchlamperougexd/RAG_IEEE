# src/rag_utils.py
from sentence_transformers import SentenceTransformer, util
import json
import os

EMBEDDINGS_DIR = "data/embeddings"
PROCESSED_DATA_DIR = "data/processed"

def create_embeddings(model_name="all-mpnet-base-v2"):
    """Создает эмбеддинги для контекстов."""