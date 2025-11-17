from chunker import build_chunks_from_collection
from embedder import Embedder
from indexer import build_faiss, save_index
from config import EMBED_MODEL

def main():
    collection_path = "data/twitter_postman.json"

    print("Extracting chunks...")
    chunks = build_chunks_from_collection(collection_path)
    texts = [c["text"] for c in chunks]
    print(f"Total chunks extracted: {len(texts)}")

    print("Embedding chunks...")
    embedder = Embedder(EMBED_MODEL)
    embeddings = embedder.embed(texts)

    print("Building FAISS index...")
    index = build_faiss(embeddings)

    print("Saving index files...")
    save_index(index, embeddings, chunks)

    print("Index built successfully!")


if __name__ == "__main__":
    main()
