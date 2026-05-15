from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.agent.recommender import (
    RecommendationAgent
)


router = APIRouter()

agent = RecommendationAgent()


class Message(BaseModel):

    role: str
    content: str


class ChatRequest(BaseModel):

    messages: List[Message]


class Recommendation(BaseModel):

    name: str
    url: str
    test_type: str


class ChatResponse(BaseModel):

    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    response = agent.handle_chat(
        request.messages
    )

    return response