from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from ingestion.document_ingestion import DocumentIngestion
import os
import google.generativeai as genai

class QuestionRequest(BaseModel):
    question: Optional[str] = Field(default="Test Question")

router = APIRouter()

@router.post("/respond")
async def respond(input: QuestionRequest):
    """
        To respond to support engineer questions.
    """
    try:
        question_text = input.question
        ingestion = DocumentIngestion()
        
        # this is done to flatten the documents list of list in chromadb
        documents = ingestion.query_documents(question_text, n_results=5)
        
        # Prepare context from documents - now documents is already a flat list
        context = "\n".join([str(doc) for doc in documents])

        gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
                    You are a helpful and an amazing support assistant. Use the provided context to answer the user's question accurately and concisely.
                    Context: {context}
                    Question: {question_text}
                    Answer:
                """
        response = model.generate_content(prompt)
        return {
            "response": response.text,
            "documents": documents
        }
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

@router.post("/classify")
async def classify(question: QuestionRequest):
    """
        To classify the ticket into a category.
    """
    return {"message": "Hello Classify"}