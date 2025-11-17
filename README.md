Semantic Search on Twitter API Documentation

This project implements a semantic search engine over the official Twitter API v2 Postman Collection.
It allows users to search the API documentation using natural language and retrieves the most relevant documentation chunks.

🚀 Features

Semantic search using Sentence Transformers

FAISS-based vector similarity search

Intelligent documentation chunking

Command-line querying

JSON output

Optional Streamlit UI

Project Structure
├── semantic_search.py
├── query.py
├── build_index.py
├── chunker.py
├── embedder.py
├── indexer.py
├── config.py
├── chunks.json
├── embeddings.npy
├── faiss_index.bin
├── data/
│   └── twitter_postman.json
└── app.py


⚙️ Installation
pip install -r requirements.txt


Place the Postman Twitter API collection file here:

data/twitter_postman.json

🧠 Build the Search Engine
1. Chunk the documentation
python build_index.py --chunk

2. Generate embeddings
python build_index.py --embed

3. Build FAISS index
python build_index.py --index

🔍 Run Semantic Search
python semantic_search.py --query "How do I fetch tweets with expansions?" --k 5

Example Output
{
  "query": "...",
  "results": [
    {
      "rank": 1,
      "score": 0.87,
      "text": "...",
      "metadata": {
        "name": "...",
        "method": "...",
        "url": "..."
      }
    }
  ]
}

🖥️ Optional Streamlit UI
streamlit run app.py

👩‍💻 Author

Srija
GitHub: https://github.com/Srija41
