from langchain.tools import tool

from ..travel_questions.retrieval import get_relevant_chunks


@tool
def search_travel_knowledge(query: str) -> list:
    """
    Use this tool for travel tips, destination advice, packing advice,
    travel safety information, transportation guidance, and questions whose
    answer may be in the travel knowledge base.
    """
    return get_relevant_chunks(query)
