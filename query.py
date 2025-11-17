import argparse
import json
from indexer import load_index
from embedder import Embedder
from config import EMBED_MODEL


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()

    index, embeddings, chunks = load_index()

    embedder = Embedder(EMBED_MODEL)
    q_emb = embedder.embed([args.query])

    distances, indices = index.search(q_emb, args.k)
    distances = distances[0]
    indices = indices[0]

    results = []
    for rank, (score, idx) in enumerate(zip(distances, indices), start=1):
        chunk = chunks[idx]
        results.append(
            {
                "rank": rank,
                "score": float(score),
                "text": chunk["text"],
                "metadata": chunk["meta"],
            }
        )

    print(json.dumps({"query": args.query, "results": results}, indent=2))


if __name__ == "__main__":
    main()
