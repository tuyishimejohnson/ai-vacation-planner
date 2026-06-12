from fastapi import FastAPI
import os
from anthropic import Anthropic

app = FastAPI()


anthropic_client = Anthropic(api_key=os.getenv("ANTRHOPIC_API_KEY"))


@app.post("/chat")
async def chat_message():

    response = anthropic_client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        temperature=0.0,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": "What is the capital of France?"}],
            }
        ],
    )

    reply = response.content[0].text

    return {"response": reply}
