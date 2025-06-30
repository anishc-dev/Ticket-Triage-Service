from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()


class Ticket(BaseModel):
    ticket_id: Optional[int] = Field(default=0)
    subject: Optional[str] = Field(default="This is a test subject")
    description: Optional[str] = Field(default="This is a test description")
    priority: Optional[str] = Field(default="Low")

@router.post("/classify")
async def classify(ticket: Ticket):
    """
        To classify the ticket into a category.
    """
    return {"message": "Hello Classify"}