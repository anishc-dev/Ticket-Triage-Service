from fastapi import FastAPI
from endpoints.listener import router as listener_router
from endpoints.chroma_db import router as chromadb_router
from ingestion.document_ingestion import DocumentIngestion
from endpoints.ticket_classifier import router as ticket_classifier_router
import logging
import traceback
from notify.notifier import observer
import os
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(listener_router)
app.include_router(chromadb_router)
app.include_router(ticket_classifier_router)

@app.on_event("startup")
async def startup_event():
    """
        Update chromadb only if db is empty.
    """
    try:
        logger.info("Starting application initialization...")
        ingestion = DocumentIngestion()
        logger.info("DocumentIngestion initialized successfully")
        
        stats = await ingestion.get_collection_stats()
        logger.info(f"Collection stats: {stats}")
        
        if stats == 0:
            logger.info("ChromaDB is empty, starting ingestion...")
            await ingestion.ingest_from_sitemap()
            logger.info("ChromaDB updated successfully")
        else:
            logger.info(f"ChromaDB already contains {stats} documents")

        logger.info("Config hot reload started successfully")
        logger.info("========================================================")
        logger.info("Application startup completed successfully")
        logger.info("========================================================")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise  # Re-raise the exception to prevent the app from starting


@app.get("/")
async def root():
    return {"message": "Welcome to the Ticket Triage Service API"}