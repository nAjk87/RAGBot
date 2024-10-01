from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from openai import OpenAI, OpenAIError, AsyncOpenAI
import pandas as pd
from pydantic import BaseModel
from sklearn import metrics
from fastapi.middleware.cors import CORSMiddleware
from streaming_response import stream_generator

import asyncio

from assistant import RagBotEventHandler

app = FastAPI()
client = AsyncOpenAI()


class RecommendationRequest(BaseModel):
    question: str
    thread_id: Optional[str] = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["x-thread-id"],
)


@app.get("/")
def read_root():
    return {"RAGBot API": "UP and RUNNING"}

@app.post("/ask-question")
async def streaming(request: RecommendationRequest) -> StreamingResponse:
    try:
        assistant = await client.beta.assistants.retrieve(
            assistant_id="asst_o4RjLqyMccAmdEPlZoQti820"
        )

        thread = await (
            client.beta.threads.create()
            if request.thread_id is None
            else client.beta.threads.retrieve(thread_id=request.thread_id)
        )

        await client.beta.threads.messages.create(
            role="user", content=request.question, thread_id=thread.id
        )
        stream = client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=RagBotEventHandler(),
        )
        return StreamingResponse(
            stream_generator(stream),
            media_type="text/event-stream",
            headers={
                "x-thread-id": thread.id,
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )
    except OpenAIError as err:
        raise HTTPException(status_code=500, detail=f"OpenAI call failed: {err}")
