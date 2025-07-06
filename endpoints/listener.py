from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional, List
from ingestion.document_ingestion import DocumentIngestion
import os
import google.generativeai as genai
from utils.logger import info, error
import time

class QuestionRequest(BaseModel):
    question: Optional[str] = Field(default="Test Question")

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/respond", response_class=HTMLResponse)
async def respond_html(request: Request):
    """
    Interactive HTML interface for querying the RAG system.
    """
    return templates.TemplateResponse("respond.html", {"request": request})

@router.post("/respond")
async def respond(input: QuestionRequest):
    """
        To respond to support engineer questions.
    """
    start_time = time.time()
    try:
        question_text = input.question
        ingestion = DocumentIngestion()
        
        # this is done to flatten the documents list of list in chromadb
        info("Querying documents from ChromaDB")
        documents = await ingestion.query_documents(question_text, n_results=5)
        
        # Prepare context from documents - now documents is already a flat list
        context = "\n".join([str(doc) for doc in documents])
        info("Context prepared")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
                    You are a helpful and an amazing support assistant. Use the provided context to answer questions accurately and concisely.
                    Context: {context}
                    Question: {question_text}
                    Answer:
                """
        response = model.generate_content(prompt)
        info("Response generated")        
        processing_time = round(time.time() - start_time, 2)
        return {
            "response": response.text,
            "documents": documents,
            "processing_time": processing_time
        }
        
    except Exception as e:
        error(f"Error: {str(e)}")
        processing_time = round(time.time() - start_time, 2)
        return {"message": f"Error: {str(e)}", "processing_time": processing_time}
