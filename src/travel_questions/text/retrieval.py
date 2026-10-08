import os
from functools import lru_cache

from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE")

@lru_cache
def _index():
    """Create the Pinecone index only when RAG is actually used."""
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc.Index(PINECONE_INDEX_NAME)


@lru_cache
def _embedding_model():
    """Load the embedding model only when RAG is actually used."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def search_travel_documents(question: str, top_k: int = 5):
    """Return the closest travel-document vectors for a question."""
    query_embedding = _embedding_model().encode(question).tolist()
    return _index().query(
        namespace=PINECONE_NAMESPACE,
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
    )


def get_relevant_chunks(question: str, top_k: int = 5) -> list[dict]:
    """Return RAG chunks in the stable shape consumed by the agent tool."""
    results = search_travel_documents(question, top_k)
    chunks = []

    for match in results["matches"]:
        metadata = match.get("metadata", {})
        text = metadata.get("text")
        if not text:
            continue

        chunks.append(
            {
                "text": text,
                "source": metadata.get("filename"),
                "score": match.get("score", 0),
            }
        )

    return chunks
