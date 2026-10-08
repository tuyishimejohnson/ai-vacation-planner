import json
from uuid import uuid4

from ...agent.agent import vacation_agent


def _tool_sources(messages) -> list[dict]:
    """Extract RAG chunks when the agent used the travel knowledge tool."""
    sources = []

    for message in messages:
        if (
            getattr(message, "type", None) != "tool"
            or getattr(message, "name", None) != "search_travel_knowledge"
        ):
            continue

        content = message.content
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                continue

        if not isinstance(content, list):
            continue

        for chunk in content:
            if not isinstance(chunk, dict) or "text" not in chunk:
                continue
            source = {
                "source": chunk.get("source"),
                "text": chunk["text"],
                "score": float(chunk.get("score", 0)),
            }
            if source not in sources:
                sources.append(source)

    return sources


def _answer_content(message) -> str:
    """Normalize LangChain text/content-block answers for the HTTP response."""
    content = message.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict) and isinstance(block.get("text"), str)
        )
    return str(content)


async def ask_travel_question(question: str, conversation_id: str | None = None):
    """Ask the tool-enabled agent through ``POST /travel/ask``.

    The agent selects the RAG tool for questions that need the indexed travel
    knowledge. Retrieved chunks are returned as response sources.
    """
    conversation_id = conversation_id or str(uuid4())
    result = await vacation_agent.ainvoke(
        {"messages": [{"role": "user", "content": question}]},
        {"configurable": {"thread_id": conversation_id}},
    )
    messages = result["messages"]

    return {
        "answer": _answer_content(messages[-1]),
        "sources": _tool_sources(messages),
        "conversation_id": conversation_id,
    }
