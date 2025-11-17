import streamlit as st
from indexer import load_index
from embedder import Embedder
from config import EMBED_MODEL

# Load index, embeddings and chunks once (cached)
@st.cache_resource
def load_resources():
    index, embeddings, chunks = load_index()
    embedder = Embedder(EMBED_MODEL)
    return index, embeddings, chunks, embedder

st.set_page_config(page_title="Twitter API Semantic Search", layout="wide")

st.title("🔍 Semantic Search on Twitter API Documentation")
st.write("Search across the entire Twitter API Postman Collection using embeddings + FAISS.")

query = st.text_input("Enter your query:", placeholder="e.g., How do I fetch tweets with expansions?")
top_k = st.slider("Number of results:", 1, 20, 5)

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        index, embeddings, chunks, embedder = load_resources()

        st.info("Running semantic search...")

        # Embed query
        q_emb = embedder.embed([query])
        scores, ids = index.search(q_emb, top_k)
        scores = scores[0]
        ids = ids[0]

        st.success(f"Top {top_k} results for: **{query}**")

        for rank, (score, idx) in enumerate(zip(scores, ids), start=1):
            chunk = chunks[idx]

            st.markdown(f"### 🟦 Result {rank}")
            st.markdown(f"**Relevance Score:** `{score:.4f}`")
            st.markdown(f"**Endpoint:** `{chunk['meta']['method']} {chunk['meta']['url']}`")
            st.markdown(f"**Chunk ID:** `{chunk['meta']['id']}`")

            with st.expander("Show Documentation Chunk"):
                st.code(chunk["text"], language="markdown")

            st.markdown("---")
