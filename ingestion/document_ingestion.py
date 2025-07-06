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
        # Initalising the chromadb for vector database
        self.client = chromadb.PersistentClient(path="./chroma_db")
        # Creating a collection for the documents
        try:
            self.collection = self.client.get_collection("netskope_docs")
        except:
            # Create the collection if it doesn't exist
            self.collection = self.client.create_collection("netskope_docs")
        self.sitemap = SitemapParser(CONFIG["SITE_URL"]).get_pages()

    async def ingest_from_sitemap(self):
        """
            Ingest documents from a sitemap and store them in a vector database
        """
        # Parse the sitemap and get the pages
        pages = SitemapParser(self.sitemap).get_pages()
        # iterate over the pages and add them to the chromadb collection
        for page in pages:
            self.ingest_page(page['url'], page['content'])

    async def ingest_page(self, url, content):
        """
            Ingest a single page into the chromadb collection
        """
        self.collection.add(
            documents=[content],
            ids=[url]
        )
    
    async def get_collection_stats(self):
        """
            Get the stats of the chromadb collection
        """
        return self.collection.count()
    
    async def query_documents(self, query_text, n_results=5):
        """
            Query documents from ChromaDB and return a flat list of documents.
        """
        try:
            result = self.collection.query(
                query_texts=[query_text],
                include=["documents"],
                n_results=n_results
            )
            # ChromaDB returns documents as a list of lists, where each sublist corresponds to a query
            # For single queries, we return the first (and only) sublist
            documents = result.get("documents", [[]])[0] if result.get("documents") else []
            return documents
        except Exception as e:
            error(f"Error querying documents: {e}")
            return []


