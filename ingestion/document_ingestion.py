"""
    Ingest documents from a sitemap and store them in a vector database
"""


import chromadb
from utils.logger import info, error
from ingestion.sitemap_parser import SitemapParser
from notify.notifier import CONFIG
import asyncio


class DocumentIngestion:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        try:
            self.collection = self.client.get_collection("netskope_docs")
        except:
            self.collection = self.client.create_collection("netskope_docs")
        self.sitemap = SitemapParser(CONFIG["SITE_URL"])

    async def ingest_from_sitemap(self):
        """
            Ingest documents from a sitemap and store them in a vector database
        """
        pages = await self.sitemap.get_pages()
        for page in pages:
            self.ingest_page(page['url'], page['content'])

    def ingest_page(self, url, content):
        """
            Ingest a single page into the chromadb collection
        """
        self.collection.add(
            documents=[content],
            ids=[url]
        )
    
    def get_collection_stats(self):
        """
            Get the stats of the chromadb collection
        """
        return self.collection.count()
    
    def query_documents(self, query_text, n_results=5):
        """
            Query documents from ChromaDB and return a flat list of documents.
        """
        result = self.collection.query(
            query_texts=[query_text],
            include=["documents"],
            n_results=n_results
        )
        documents = result.get("documents", [[]])[0] if result.get("documents") else []
        return documents
       


