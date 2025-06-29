from fastapi import FastAPI, Response
from endpoints.listener import router
from ingestion.document_ingestion import DocumentIngestion
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """
        Update chromadb only if db is empty.
    """
    try:
        logger.info("Starting application initialization...")
        ingestion = DocumentIngestion()
        logger.info("DocumentIngestion initialized successfully")
        
        stats = ingestion.get_collection_stats()
        logger.info(f"Collection stats: {stats}")
        
        if stats == 0:
            logger.info("ChromaDB is empty, starting ingestion...")
            ingestion.ingest_from_sitemap()
            logger.info("ChromaDB updated successfully")
        else:
            logger.info(f"ChromaDB already contains {stats} documents")
            
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise  # Re-raise the exception to prevent the app from starting

@app.get("/")
async def root():
    return {"message": "Welcome to the Ticket Triage Service API"}

@app.get("/chromadb")
async def chromadb_html():
    try:
        ingestion = DocumentIngestion()
        count = ingestion.get_collection_stats()
        results = ingestion.collection.get(limit=min(10, count), include=["documents"])
        ids = results["ids"]
        html = f"""
        <html><head><title>ChromaDB Contents</title></head><body>
        <h2>ChromaDB Collection: netskope_docs</h2>
        <p>Total documents: <b>{count}</b></p>
        <h3>Sample Document IDs (first 10):</h3>
        <ul>
        {''.join(f'<li>{doc_id}</li>' for doc_id in ids)}
        </ul>
        </body></html>
        """
        return Response(content=html, media_type="text/html")
    except Exception as e:
        logging.error(f"Error during chromadb_html: {e}")
        return Response(content=f"Error: {str(e)}", media_type="text/plain")