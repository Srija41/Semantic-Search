import faiss
import numpy as np
import json
from config import INDEX_PATH, EMBEDDINGS_PATH, CHUNKS_METADATA


def build_faiss(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index


def save_index(index, embeddings, chunks):
    faiss.write_index(index, INDEX_PATH)
    np.save(EMBEDDINGS_PATH, embeddings)
    with open(CHUNKS_METADATA, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)


def load_index():
    index = faiss.read_index(INDEX_PATH)
    embeddings = np.load(EMBEDDINGS_PATH)

    with open(CHUNKS_METADATA, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    return index, embeddings, chunks
