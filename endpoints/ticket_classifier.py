import datetime
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional
from google import generativeai
import os
import re
import json
from database.database import insert_into_table, create_table, TABLE_COLUMNS, get_tickets
import logging
from notify.notifier import CONFIG
from utils.logger import info, error
import time

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class Ticket(BaseModel):
    ticket_id: Optional[str] = Field(default="0")
    subject: str = Field(default="This is a test subject")
    description: str = Field(default="This is a test description")
    priority: str = Field(default="Low")

@router.get("/classify", response_class=HTMLResponse)
async def classify_html(request: Request):
    """
    Interactive HTML interface for ticket classification.
    """
    return templates.TemplateResponse("classify.html", {"request": request})

@router.post("/classify")
async def classify(ticket: Ticket):
    """
        To classify the ticket into a category.
    """
    start_time = time.time()
    try:
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            error("No AI key defined")
            processing_time = round(time.time() - start_time, 2)
            return {"message": "No AI key defined", "processing_time": processing_time}
        info("AI key defined")
        generativeai.configure(api_key=gemini_key)
        question = ticket.subject + " " + ticket.description
        
        
        prompt = f""" 
        You are an amazing classifier. Given a ticket description, classify it into a category and urgency.
        The category must be one of: {CONFIG["CATEGORIES"]}
        The priority must be one of: {CONFIG["PRIORITY"]}
        Question: {question}
        
        Respond with ONLY:
        Category: [category_name]
        Priority: [priority_level]
        """
        
        model = generativeai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        # Simple regex parsing
        category_match = re.search(r'Category:\s*([^\n]+)', response.text, re.IGNORECASE)
        priority_match = re.search(r'Priority:\s*([^\n]+)', response.text, re.IGNORECASE)
        
        if not category_match or not priority_match:
            error(f"No category or priority found in response: {response.text}")
            processing_time = round(time.time() - start_time, 2)
            return {"message": "No category or priority found in response", "processing_time": processing_time}
        
        category_value = category_match.group(1).strip() 
        priority_value = priority_match.group(1).strip()
        
        info(f"Parsed classification - Category: {category_value}, Priority: {priority_value}")
        
        metadata = create_metadata(category_value, priority_value, ticket.ticket_id) 
        await create_table("TICKET_METADATA", TABLE_COLUMNS["TICKET_METADATA"])
        await insert_into_table("TICKET_METADATA", list(metadata.keys()), list(metadata.values()))   
        info(f'Successfully inserted metadata of ticket {ticket.ticket_id} into the database')

        processing_time = round(time.time() - start_time, 2)
        return {
            'message': f'Successfully Classified and inserted metadata of ticket {ticket.ticket_id} into the database',
            'classification': {
                'category': category_value,
                'priority': priority_value,
                'ticket_id': ticket.ticket_id
            },
            'processing_time': processing_time
        }
        
    except Exception as e:
        error(f"Error in classification: {str(e)}")
        processing_time = round(time.time() - start_time, 2)
        return {"message": f"Error during classification: {str(e)}", "processing_time": processing_time}

def create_metadata(category_value, priority_value, ticket_id):
    """
        To create the metadata for the ticket.
    """
    metadata = {
        "ticket_id": ticket_id,
        "category": category_value,
        "priority": priority_value,
        "query_time": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    return metadata

@router.get("/tickets")
async def get_tickets_endpoint():
    try:
        tickets = await get_tickets()
        return {"tickets": tickets, "count": len(tickets)}
    except Exception as e:
        error(f"Error retrieving tickets: {str(e)}")
        return {"message": f"Error retrieving tickets: {str(e)}"}