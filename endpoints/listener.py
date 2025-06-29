from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from ingestion.document_ingestion import DocumentIngestion

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
        
        result = ingestion.collection.query(
            query_texts=[question_text],
            include=["documents"],
            n_results=10
        )
        documents = result.get("documents", [])
        return {"documents": documents}     
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

@router.post("/classify")
async def classify(question: QuestionRequest):
    """
        To classify the ticket into a category.
    """
    return {"message": "Hello Classify"}