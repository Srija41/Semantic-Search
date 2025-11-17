from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts, batch_size=32):
        emb = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
        )
        norms = np.linalg.norm(emb, axis=1, keepdims=True)
        norms[norms == 0] = 1
        emb = emb / norms
        return emb.astype("float32")
