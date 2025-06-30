from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from google import generativeai
import os
from configuration.classify import categories, priority

router = APIRouter()

class Ticket(BaseModel):
    ticket_id: Optional[int] = Field(default=0)
    subject: str = Field(default="This is a test subject")
    description: str = Field(default="This is a test description")
    priority: str = Field(default="Low")

@router.post("/classify")
async def classify(ticket: Ticket):
    """
        To classify the ticket into a category.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        return{"message: No AI key defined"}
    generativeai.configure(api_key=gemini_key)
    question = ticket.subject + ticket.description
    prompt = f""" 
            You are an amazing classifier. Given a ticke description and you need to classify it into a category and urgency. 
            The category is defined under {categories}
            The priority is defined under {priority}
            Question: {question}
            Answer:
    """
    model = generativeai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return {"message": response.text}