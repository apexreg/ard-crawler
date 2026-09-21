from __future__ import annotations
from sentence_transformers import SentenceTransformer
from typing import List

# Use a small, fast model for 384-dim embeddings
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_model: SentenceTransformer | None = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def embed_text(text: str) -> List[float]:
    """
    Embed a text string into a 384-dim vector (list of floats).
    """
    model = get_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()
