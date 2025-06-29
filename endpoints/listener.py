from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List

class Ticket(BaseModel):
    ticket: Optional[int] = Field(default=None)
    message: Optional[str] = Field(default=None)   
    user_id: Optional[int] = Field(default=None)

router = APIRouter()

@router.post("/respond")
async def respond(ticket: Ticket):
    """
        To respond to support engineer questions.
    """
    return {"message": "Hello Respond"}

@router.post("/classify")
async def classify(ticket: Ticket):
    """
        To classify the ticket into a category.
    """
    return {"message": "Hello Classify"}