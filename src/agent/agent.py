from typing import NotRequired

from langchain.agents import AgentState, create_agent
from langgraph.checkpoint.memory import InMemorySaver

from ..tools.countries import get_countries_and_cities
from ..tools.exchange_rate import get_exchange_rate
from ..tools.places import search_places
from ..tools.travel_knowledge import search_travel_knowledge
from ..tools.weather import get_current_weather


class VacationAgentState(AgentState):
    destination: NotRequired[str]
    origin_currency: NotRequired[str]


checkpointer = InMemorySaver()

vacation_agent = create_agent(
    model="claude-haiku-4-5",
    tools=[
        get_current_weather,
        search_places,
        search_travel_knowledge,
        get_countries_and_cities,
        get_exchange_rate,
    ],
    system_prompt=(
        "You are a vacation planning assistant. "
        "Use the available tools whenever they can provide "
        "more accurate or current information. "
        "Use the travel knowledge tool for information contained "
        "in the travel knowledge base, including travel tips, packing, "
        "safety, and transportation guidance. When a question could be "
        "answered by that knowledge base, call the tool before answering "
        "and ground your answer in its results. "
        "Use weather for current weather information. "
        "Use exchange rates for currency conversion. "
        "Use places for location and place searches. "
        "Use country information when destination or country "
        "details are needed. "
        "Remember information already provided in the conversation. "
        "Do not invent information that should come from a tool."
    ),
    state_schema=VacationAgentState,
    checkpointer=checkpointer,
)


