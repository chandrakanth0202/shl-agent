from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.services.hybrid_retriever import hybrid_recommend
from app.services.guardrails import detect_prompt_injection
from app.services.response_generator import generate_reply
from app.services.response_formatter import format_recommendations
from app.services.comparison import compare_assessments

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

def needs_clarification(text: str):

    text = text.lower().strip()

    vague_inputs = [
        "assessment",
        "test",
        "hiring",
        "need assessment",
        "need test"
    ]

    return text in vague_inputs

@router.post("/chat")
def chat(req: ChatRequest):

    latest_message = req.messages[-1].content

    # Prompt injection protection
    if detect_prompt_injection(latest_message):

        return {
            "reply": "I can only recommend assessments from the SHL catalog.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Assessment comparison handling
    comparison_reply = compare_assessments(latest_message)

    if comparison_reply:

        return {
            "reply": comparison_reply,
            "recommendations": [],
            "end_of_conversation": True
        }

    # Combine full conversation history
    conversation_text = " ".join(
        [
            message.content
            for message in req.messages
            if message.role == "user"
        ]
    )

    # Clarification handling
    if needs_clarification(latest_message):

        return {
            "reply": (
                "Please provide the role, seniority level, "
                "and assessment type required."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # Hybrid retrieval
    recommendations = hybrid_recommend(conversation_text)

    # No results found
    if not recommendations:

        return {
            "reply": (
                "I could not find suitable SHL assessments "
                "for the provided requirements."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # Format response schema
    recommendations = format_recommendations(recommendations)

    # Generate recruiter-style reply
    reply = generate_reply(
        conversation_text,
        recommendations
    )

    return {
        "reply": reply,
        "recommendations": recommendations[:10],
        "end_of_conversation": True
    }