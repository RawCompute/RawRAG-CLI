from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> np.ndarray:
    """
    Get the embedding for a given text using the SentenceTransformer model.
    """
    embeddings = model.encode(text)
    return np.array(embeddings, dtype=np.float32)