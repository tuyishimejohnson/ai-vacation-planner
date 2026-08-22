# travel/service.py

import os

from dotenv import load_dotenv

from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from anthropic import Anthropic

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE")


pc = Pinecone(api_key=PINECONE_API_KEY)
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

index = pc.Index(PINECONE_INDEX_NAME)


embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


TRAVEL_SYSTEM_PROMPT = """
You are a travel information assistant.

Answer the user's question using ONLY the information
provided in the retrieved context.

Do not invent facts.

If the retrieved context does not contain enough information
to answer the question, say that the available travel
information does not contain enough information to answer
the question.

Keep answers concise and useful.
"""


# Pinecone retrieval function
def search_travel_documents(
    question: str,
    top_k: int = 5,
):
    query_embedding = embedding_model.encode(question).tolist()

    results = index.query(
        namespace=PINECONE_NAMESPACE,
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
    )

    return results


# Get relevant chunks
def get_relevant_chunks(
    question: str,
    top_k: int = 5,
):
    results = search_travel_documents(
        question,
        top_k,
    )

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


# Build context for the claude
def build_context(chunks):
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(f"""
SOURCE {i}
Source: {chunk["source"]}

Content:
{chunk["text"]}
""")

    return "\n".join(context_parts)


# Generate travel answer using claude
def generate_travel_answer(
    question: str,
    chunks,
):
    context = build_context(chunks)

    prompt = f"""
User question:

{question}

Retrieved travel information:

{context}

Answer the user's question using the retrieved
travel information.
"""

    response = claude_client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        temperature=0.2,
        system=TRAVEL_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.content[0].text


# Ask travel question function
def ask_travel_question(question: str):
    chunks = get_relevant_chunks(
        question=question,
        top_k=5,
    )

    if not chunks:
        return {
            "answer": (
                "I could not find relevant information "
                "in the available travel documents."
            ),
            "sources": [],
        }

    answer = generate_travel_answer(
        question=question,
        chunks=chunks,
    )

    return {
        "answer": answer,
        "sources": [
            {
                "source": chunk["source"],
                "text": chunk["text"],
                "score": chunk["score"],
            }
            for chunk in chunks
        ],
    }
